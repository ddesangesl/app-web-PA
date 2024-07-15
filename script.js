// Function to generate table rows
function generateTableRows(data) {
    // Listage des dates
    const values = Object.values(data);
    var dateList = values.map(game => game.GAME_DATE);
    dateList = [...new Set(dateList)];
    for (var date in dateList) {
        var tableBody = document.getElementById("table-body");

        // Listage des match s'étant joué le jour de date
        var entries = Object.entries(data);
        var filteredEntries = entries.filter(([key, value]) => value.GAME_DATE == dateList[date]);
        var gameList = Object.fromEntries(filteredEntries);

        var row = "<tr> <td colspan='1' class=chakra-petch-bold style='padding-top : 38px; font-weight:800'>" + new Date(dateList[date]).toLocaleDateString() + "</td>";

        for (var game in gameList) {
            var homePoints = gameList[game].H_POINTS > gameList[game].A_POINTS ? 800 : 200
            var awayPoints = gameList[game].A_POINTS > gameList[game].H_POINTS ? 800 : 200

            var predict = gameList[game].HOME_WON == gameList[game].PRED ? "<span class='badge badge-success'>Prédit</span>" : "";

            row += "<tr>" +
                "<td><img src='img/" + gameList[game].H_teamName + ".png ' class='logoTeam'></td> " +
                "<td>" + gameList[game].H_teamName + "</td>" +
                "<td class=chakra-petch-bold style='font-weight:" + homePoints + "'>" + gameList[game].H_POINTS + "</td>" +
                "<td><span class='badge badge-primary'>VS</span></td>" +
                "<td class=chakra-petch-bold style='font-weight:" + awayPoints + "'>" + gameList[game].A_POINTS + "</td>" +
                "<td> " + gameList[game].A_teamName + "</td>" +
                "<td><img src='img/" + gameList[game].A_teamName + ".png ' class='logoTeam'></td> " +
                "<td>" + predict + "</td>" +
                "</tr>";
        }
        tableBody.innerHTML += row;
    }

}



function main() {
    let data;
    fetch('GB_prediction.json')
        .then(response => response.json())
        .then(jsonData => {
            generateTableRows(jsonData)
            //return data
        })
        .catch(error => {
            console.error('Erreur lors du chargement du fichier JSON:', error);
        });
}