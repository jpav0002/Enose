import base64
from github import Github
from pprint import pprint

# pygithub object
g = Github("b5011de347845175cc946f73811090cdb1546ddd")
# get that user by username
user = g.get_user()

for repo in user.get_repos():

    if (repo.name == "Enose"):
        repoClone = repo

#Commit it
index = repoClone.index
index.add_all()
index.write()
author = pygit2.Signature("jpav0002", "jpav0002@red.ujaen.es")
commiter = pygit2.Signature("jpav0002", "jpav0002@red.ujaen.es")
tree = index.write_tree()
oid = repoClone.create_commit('refs/heads/master', author, commiter, "test",tree,[repoClone.head.get_object().hex])
remote = repoClone.remotes["origin"]
credentials = pygit2.UserPass("jpav0002", "Jp0792av.")
remote.credentials = credentials

callbacks=pygit2.RemoteCallbacks(credentials=credentials)

remote.push(['refs/heads/master'],callbacks=callbacks)
