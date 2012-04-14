import pprint
import facebook

oauth_access_token='AAAEASRPSx7oBADFK6uKeNZAYLQZAMPyK5m9X9vtqkC2ZA2PDndDz00onDAQ7OPFdGrZCPANsDdFZBffqAgXVPj37ny5XpyohBCkmHHQjNJwZDZD'
graph = facebook.GraphAPI(oauth_access_token)
profile = graph.get_object("me/inbox")
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(profile)
