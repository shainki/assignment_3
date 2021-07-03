function makeGetRequest(path) {
    axios.get(path).then(
        (response) => {
            var result = response.valid_data;
            console.log(result);
        },
        (error) => {
            console.log(error);
        }
    );
}
makeGetRequest('http://127.0.0.1:5000/list');