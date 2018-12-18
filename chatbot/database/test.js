db.quote.insert({author:"shakespeare", quote: "To be or not to be..."})
db.createUser(
   {
     user: "chatbot",
     pwd: "passw",
     roles: [ "readWrite", "dbAdmin" ]
   }
)
