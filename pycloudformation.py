
import json

class CloudFormationTemplate(dict):
    def __init__(self, *args, **kwargs):               
        for k, v in kwargs.items():
            if type(v) == dict:
                new_v = CloudFormationTemplate(v)
                new_v.__name__ = k
                kwargs[k] = new_v

            if isinstance(v, CloudFormationTemplate):
                v.__name__ = k

        super(CloudFormationTemplate, self).__init__(**kwargs)

        for i, a in enumerate(args):
            if isinstance(a, dict):
                self.update(a)
            else:
                raise ValueError("Argument %d must be type dict" % i)

    def template(self, pretty=False):
        if pretty:
            return json.dumps(self, sort_keys=True,  indent=2, separators=(',', ': '))
        else:
            return json.dumps(self)

    def __getattr__(self, k):
        if k[0] == '_' or self.__dict__.has_key(k):
            return self.__dict__[k]
        else:
            return self[k]
        
    def __setattr__(self, k, v):
        if k[0] == '_' or self.__dict__.has_key(k):
            self.__dict__[k] = v
        else:
            v.__name__ = k
            self[k] = v
    
    def __repr__(self):
        return self.__name__

def ref(reference):
    if isinstance(reference, CloudFormationTemplate):
        return dict(Ref = str(reference))
    elif isinstance(reference, str):
        return dict(Ref = reference)
    else:
        raise ValueError("Unknown reference type")

def get_att(object, attribute):
    if isinstance(object, CloudFormationTemplate):
        return {"Fn::GetAtt": [str(object), attribute]}
    elif isinstance(object, str):
        return {"Fn::GetAtt": [object, attribute]}
    else:
        raise ValueError("Unknown object type")

def find_in_map(map, kay, field):
    if isinstance(object, str):
        return {"Fn::GetAtt": [object, attribute]}
    else:
        name = getattr(map, '__name__', None)
        if name is not None:
            return { "Fn::FindInMap" : [name, kay, field] }
        else:
            raise ValueError("Unknown map type: %s" % str(map))


def join(arg0, arg1=None):
    if isinstance(arg0, str):
        assert(isinstance(arg1, list) or isinstance(arg1, tupple))
        
        return {"Fn::Join": [arg0, arg1]}
    elif isinstance(arg0, list) or isinstance(arg0, tupple):
    
        return {"Fn::Join": ["", arg0]}
    else:
        raise ValueError("Unknown arg types")

def base64(arg):
    return {"Fn::Base64": arg}

def get_azs():
    return {"Fn::GetAZs": ""}
