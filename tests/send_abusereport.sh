if [ "$1" == "" ]
then
	echo "Usage: $0 <sample file.json>"
	exit 1
fi

curl -d "@$1" -H "Content-Type: application/json" -X POST -H "Authorization: Token test" http://localhost:8080/

