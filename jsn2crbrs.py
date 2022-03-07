import click, simplejson as json

@click.command()
@click.option('--infile', help='json file to use for cerberus schema generation.')

def main(infile):

    try:
        schema = recursive(json.loads(open(infile,"r").read()))
        print(json.dumps(schema, indent=4, sort_keys=False))
        
    except Exception as e:
        raise e

def recursive(rin):

    rout = {}

    for e in rin:

        if isinstance(rin[e], dict):
            rout[e] = {"type" : "dict", "schema": recursive(rin[e])}
        elif isinstance(rin[e], list):

            for x in rin[e]:

                if isinstance(x, dict):
                    rout[e] = {"type" : "list", "schema": {"type" : "dict", "schema": recursive(x)}}
                    break
                elif isinstance(x, list):
                    rout[e] = {"type" : "list", "schema": {"type" : "list", "schema": recursive(x)}}
                elif isinstance(x, bool):
                    rout[e] = {"type" : "list", "schema": {"type" : "boolean"}}
                elif isinstance(x, int):
                    rout[e] = {"type" : "list", "schema": {"type" : "integer"}}
                elif isinstance(x, float):
                    rout[e] = {"type" : "list", "schema": {"type" : "float"}}
                else:
                    rout[e] = {"type" : "list", "schema": {"type" : "string"}}

        elif isinstance(rin[e], bool):
            rout[e] = {"type" : "boolean"}
        elif isinstance(rin[e], int):
            rout[e] = {"type" : "integer"}
        elif isinstance(rin[e], float):
            rout[e] = {"type" : "float"}
        else:
            rout[e] = {"type" : "string"}

    return rout

if __name__ == "__main__":

    main()
