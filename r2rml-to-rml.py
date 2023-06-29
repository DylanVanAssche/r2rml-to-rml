#!/usr/bin/env python3

import argparse
from rdflib import Graph, BNode, Namespace, Literal, RDF

R2RML = Namespace('http://www.w3.org/ns/r2rml#')
RML = Namespace('http://semweb.mmlab.be/ns/rml#')
D2RQ = Namespace('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#')


def convert_r2rml_to_rml(mapping_file: str, output_path: str, driver: str,
                         rdb_host: str, rdb_port: int, rdb_name: str,
                         rdb_username: str, rdb_password: str):
    # Compatibility with R2RML mapping files
    # Replace rr:logicalTable with rml:logicalSource + D2RQ description
    # and rr:column with rml:reference
    g = Graph()
    g.bind('rr', R2RML)
    g.bind('rml', RML)
    g.bind('d2rq', D2RQ)
    g.bind('rdf', RDF)
    g.parse(mapping_file)

    dsn = f'{driver}://{rdb_host}:{rdb_port}/{rdb_name}'

    # rr:logicalTable --> rml:logicalSource
    for triples_map_iri, p, o in g.triples((None, RDF.type,
                                            R2RML.TriplesMap)):
        logical_source_iri = BNode()
        d2rq_rdb_iri = BNode()
        logical_table_iri = g.value(triples_map_iri,
                                    R2RML.logicalTable)
        if logical_table_iri is None:
            break

        table_name_literal = g.value(logical_table_iri,
                                     R2RML.tableName)
        sql_query_literal = g.value(logical_table_iri,
                                    R2RML.sql_query_literal)
        if table_name_literal is None and sql_query_literal is None:
            break

        g.add((d2rq_rdb_iri, D2RQ.jdbcDSN, Literal(dsn)))
        g.add((d2rq_rdb_iri, D2RQ.jdbcDriver, Literal(driver)))
        g.add((d2rq_rdb_iri, D2RQ.username, Literal(rdb_username)))
        g.add((d2rq_rdb_iri, D2RQ.password, Literal(rdb_password)))
        g.add((d2rq_rdb_iri, RDF.type, D2RQ.Database))
        g.add((logical_source_iri, R2RML.sqlVersion, R2RML.SQL2008))
        if table_name_literal is not None:
            g.add((logical_source_iri, R2RML.tableName,
                   table_name_literal))
        if sql_query_literal is not None:
            g.add((logical_source_iri, R2RML.sqlQuery,
                   sql_query_literal))
        g.add((logical_source_iri, RML.source, d2rq_rdb_iri))
        g.add((logical_source_iri, RDF.type, RML.LogicalSource))
        g.add((triples_map_iri, RML.logicalSource, logical_source_iri))
        g.remove((triples_map_iri, R2RML.logicalTable,
                  logical_table_iri))
        if table_name_literal is not None:
            g.remove((logical_table_iri, R2RML.tableName,
                      table_name_literal))
        if sql_query_literal is not None:
            g.remove((logical_table_iri, R2RML.sqlQuery,
                      sql_query_literal))
        g.remove((logical_table_iri, RDF.type, R2RML.LogicalTable))
        g.remove((logical_table_iri, R2RML.sqlVersion, R2RML.SQL2008))

    # rr:column --> rml:reference
    for s, p, o in g.triples((None, R2RML.column, None)):
        g.add((s, RML.reference, o))
        g.remove((s, p, o))

    # rml:referenceFormulation is not needed for RDBs
    for s, p, o in g.triples((None, RML.referenceFormulation, None)):
        g.remove((s, p, o))

    g.serialize(destination=output_path, format='turtle')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copyright by (c) '
                                                 'Dylan Van Assche (2023), '
                                                 'available under the MIT '
                                                 'license')
    parser.add_argument('--mapping-file', type=str, required=True,
                        help='Path to R2RML mapping file')
    parser.add_argument('--output-path', type=str, required=True,
                        help='Path to output the RML mapping file')
    parser.add_argument('--rdb-driver', type=str, required=True,
                        help='RDB Driver to use')
    parser.add_argument('--rdb-host', type=str, required=True,
                        help='RDB host')
    parser.add_argument('--rdb-port', type=int, required=True,
                        help='RDB port')
    parser.add_argument('--rdb-name', type=str, required=True,
                        help='RDB database name')
    parser.add_argument('--rdb-username', type=str, required=True,
                        help='RDB database username')
    parser.add_argument('--rdb-password', type=str, required=True,
                        help='RDB database password')
    args = parser.parse_args()
    convert_r2rml_to_rml(args.mapping_file, args.output_path, args.rdb_driver,
                         args.rdb_host, args.rdb_port, args.rdb_name,
                         args.rdb_username, args.rdb_password)
