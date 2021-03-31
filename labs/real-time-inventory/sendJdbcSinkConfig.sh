if [[ $# -ne 1 ]]
then
  echo "Usage: need the URL of the Kafka connect listener"
  exit 1
fi
echo Let delete existing definition 

set -x
curl -X DELETE  -w "%{http_code}" -H 'content-type: application/json' http://$1/connectors/jdbc-sink-connector
echo '\n'
curl -X POST  -w "%{http_code}" -H 'content-type: application/json' -d@"./db2-sink-config.json" http://$1/connectors
echo '\n'
curl  -w "%{http_code}" -H 'content-type: application/json' http://$1/connectors