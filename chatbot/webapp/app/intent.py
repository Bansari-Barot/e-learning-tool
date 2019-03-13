import json
import csv


# from intent import create_intent
# if __name__ == "__main__":
#     file="f1.csv"
#     create_intent.create_json(file)


class create_intent():
    def create_json(csv_file):
        rows=[]
        with open(csv_file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                rows.append(row)

        print(rows)
        count=0
        for i in rows:

            data={
              "name": i[0],
              "responses": [
                {

                  "messages": [
                    {

                      "speech": i[-1]
                    }
                  ],

                }
              ],

              "userSays": [

              ]

            }
            questions=i[1:len(i)-1]
            for j in questions:
                data['userSays'].append({

              "data": [
                {
                  "text": j
                }
              ]

            })
            count+=1
            filename="data_"+str(count)+".json"
            with open(filename,'w') as outfile:
                json.dump(data, outfile)
