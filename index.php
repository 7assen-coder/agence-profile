<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plan des places - Groupe 10</title>

    <style>
        html, body {
            height: 100%;
            width: 100%;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Calibre", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f7f6;
            color: #1e293b;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .wrapper {
            width: 100%;
            max-width: 850px;
            padding: 20px;
        }

        /* Conteneur principal avec effet d'ombre douce */
        .container {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08), 0 4px 6px rgba(0, 0, 0, 0.04);
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
        }

        .grid-50 {
            flex: 1;
            min-width: 320px;
        }

        #seat-map {
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }

        .front-indicator {
            background-color: #0093E9;
            background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
            color: #ffffff;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
            font-size: 20px;
            font-weight: 700;
            padding: 14px 0;
            text-align: center;
            border-radius: 50px;
            margin-bottom: 15px;
        }

        /* États et styles des sièges */
        div.seatCharts-seat {
            color: #FFFFFF;
            cursor: pointer;
            height: 4em;
            width: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 4px;
            transition: all 0.2s ease;
        }

        div.seatCharts-seat:hover {
            transform: translateY(-2px);
            filter: brightness(0.95);
        }

        /* Place libre : Vert */
        div.seatCharts-seat.available {
            background: #10b981;
        }

        /* Place sélectionnée : Bleu / Turquoise */
        div.seatCharts-seat.selected {
            background: #3b82f6;
            color: #ffffff;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4);
        }

        /* Place non disponible (réservée ou payée) : Orange ou Rouge */
        div.seatCharts-seat.unavailable {
            cursor: not-allowed;
        }
        
        div.seatCharts-seat.reservee {
            background: #f59e0b; /* Réservée */
        }

        div.seatCharts-seat.payee {
            background: #ef4444; /* Payée */
        }

        div.seatCharts-space {
            background-color: transparent;
            width: 35px;
        }

        .booking-details {
            padding: 10px;
        }

        .booking-details h2 {
            font-size: 19px;
            font-weight: 700;
            color: #0f172a;
            margin: 20px 0 16px 0;
        }

        .booking-details h3 {
            font-size: 14px;
            color: #475569;
            margin-bottom: 6px;
        }

        #selected-seats {
            min-height: 8em;
            max-height: 12em;
            overflow: auto;
            background: #f8fafc;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            color: #0f172a;
            font-weight: 600;
            font-size: 13px;
            list-style: none;
            padding-left: 10px;
            margin-bottom: 15px;
        }

        .text-muted {
            color: #64748b;
            text-shadow: none;
            font-size: 14px;
        }

        #checkout-button {
            margin: 10px 0;
            padding: 14px 0;
            width: 100%;
            text-align: center;
            text-transform: uppercase;
            color: #fff;
            border-radius: 8px;
            font-weight: 600;
            background-image: linear-gradient(to right, #77A1D3 0%, #79CBCA 51%, #77A1D3 100%);
            border: none;
            cursor: pointer;
            transition: background-position 0.4s ease;
        }

        #reset-btn {
            width: 100%;
            margin-top: 10px;
            padding: 14px 0;
            text-align: center;
            text-transform: uppercase;
            color: #fff;
            border-radius: 8px;
            font-weight: 600;
            background-image: linear-gradient(to right, #06beb6 0%, #48b1bf 51%, #06beb6 100%);
            border: none;
            cursor: pointer;
            transition: background-position 0.4s ease;
        }

        #checkout-button:hover, #reset-btn:hover {
            background-position: right center;
        }

        /* Couleurs de la légende */
        .color-box.libre { background: #10b981; width: 16px; height: 16px; display: inline-block; border-radius: 4px; vertical-align: middle; }
        .color-box.reservee { background: #f59e0b; width: 16px; height: 16px; display: inline-block; border-radius: 4px; vertical-align: middle; }
        .color-box.payee { background: #ef4444; width: 16px; height: 16px; display: inline-block; border-radius: 4px; vertical-align: middle; }
        .color-box.selectionnee { background: #3b82f6; width: 16px; height: 16px; display: inline-block; border-radius: 4px; vertical-align: middle; }
    </style>
</head>

<body>
    <div class="wrapper">
        <div class="container">
            <div class="grid-50">
                <div id="seat-map">
                    <div class="front-indicator">Affichage des places du bus</div>
                    <h4 class="text-muted fw-bold text-center" style="margin: 0.8em">De l'avant du bus</h4>
                    
                    <div class="bus-layout" style="display: flex; justify-content: center;">
                        <div class="bus-cabin" id="bus-grid"></div>
                    </div>

                    <h4 class="text-muted fw-bold text-center" style="margin: 0.8em">Fond du bus</h4>
                </div>
            </div>

            <div class="grid-50">
                <div class="booking-details">
                    

                    <h3>Places sélectionnées (<span id="counter">0</span>) :</h3>
                    <ul id="selected-seats">Aucune place sélectionnée</ul>

                   

                    <button type="button" id="checkout-button" onclick="validerReservation()">Valider</button>

                    <div id="legend">
                        <h3>Légende :</h3>
                        <ul style="list-style: none; padding-left: 0; font-size: 13px;">
                            <li style="margin-top: 8px;">
                                <span class="color-box libre"></span> Libre
                            </li>
                            <li style="margin-top: 8px;">
                                <span class="color-box selectionnee"></span> Sélectionnée
                            </li>
                            <li style="margin-top: 8px;">
                                <span class="color-box reservee"></span> Réservée
                            </li>
                            <li style="margin-top: 8px;">
                                <span class="color-box payee"></span> Payée
                            </li>
                        </ul>
                    </div>

                    <button id="reset-btn" type="button" onclick="resetSelection()">Réinitialiser</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // États des 12 places du bus
        const places = [
            { id: 1, etat: "libre" },
            { id: 2, etat: "libre" },
            { id: 3, etat: "reservee" },
            { id: 4, etat: "payee" },
            { id: 5, etat: "reservee" },
            { id: 6, etat: "libre" },
            { id: 7, etat: "payee" },
            { id: 8, etat: "libre" },
            { id: 9, etat: "libre" },
            { id: 10, etat: "libre" },
            { id: 11, etat: "libre" },
            { id: 12, etat: "libre" }
        ];

        function genererPlan() {
            const cabin = document.getElementById('bus-grid');
            cabin.innerHTML = '';

            for (let i = 0; i < places.length; i += 4) {
                const row = document.createElement('div');
                row.style.display = 'flex';
                row.style.alignItems = 'center';
                row.style.justifyContent = 'center';
                row.style.margin = '8px 0';

                // Sièges 1 et 2 (ou 5 et 6, etc.)
                for (let j = 0; j < 2; j++) {
                    const placeIndex = i + j;
                    if (placeIndex < places.length) {
                        const p = places[placeIndex];
                        const seat = document.createElement('div');
                        seat.textContent = p.id;
                        seat.setAttribute('data-id', p.id);

                        if (p.etat === "libre") {
                            seat.className = "seatCharts-seat available";
                            seat.onclick = function() { toggleSelection(this); };
                        } else if (p.etat === "reservee") {
                            seat.className = "seatCharts-seat unavailable reservee";
                        } else if (p.etat === "payee") {
                            seat.className = "seatCharts-seat unavailable payee";
                        }
                        row.appendChild(seat);
                    }
                }

                // Couloir
                const aisle = document.createElement('div');
                aisle.className = "seatCharts-space";
                row.appendChild(aisle);

                // Sièges 3 et 4 (ou 7 et 8, etc.)
                for (let j = 2; j < 4; j++) {
                    const placeIndex = i + j;
                    if (placeIndex < places.length) {
                        const p = places[placeIndex];
                        const seat = document.createElement('div');
                        seat.textContent = p.id;
                        seat.setAttribute('data-id', p.id);

                        if (p.etat === "libre") {
                            seat.className = "seatCharts-seat available";
                            seat.onclick = function() { toggleSelection(this); };
                        } else if (p.etat === "reservee") {
                            seat.className = "seatCharts-seat unavailable reservee";
                        } else if (p.etat === "payee") {
                            seat.className = "seatCharts-seat unavailable payee";
                        }
                        row.appendChild(seat);
                    }
                }
                cabin.appendChild(row);
            }
        }

        function toggleSelection(element) {
            element.classList.toggle("selected");

            const selectedSeats = document.querySelectorAll('.seatCharts-seat.available.selected');
            const selectedList = document.getElementById('selected-seats');
            const counter = document.getElementById('counter');
            const total = document.getElementById('total');

            selectedList.innerHTML = '';

            if (selectedSeats.length > 0) {
                let listHtml = '';
                selectedSeats.forEach(seat => {
                    listHtml += `<li>Siège ${seat.getAttribute('data-id')}</li>`;
                });
                selectedList.innerHTML = listHtml;
                counter.textContent = selectedSeats.length;
                total.textContent = selectedSeats.length * 200; // Prix unitaire en MRU
            } else {
                selectedList.textContent = 'Aucune place sélectionnée';
                counter.textContent = '0';
                total.textContent = '0';
            }
        }

        function resetSelection() {
            document.querySelectorAll('.seatCharts-seat.available.selected').forEach(seat => {
                seat.classList.remove("selected");
            });
            document.getElementById('selected-seats').textContent = 'Aucune place sélectionnée';
            document.getElementById('counter').textContent = '0';
            document.getElementById('total').textContent = '0';
        }

        function validerReservation() {
            if (document.getElementById('counter').textContent === '0') {
                alert('Veuillez sélectionner au moins une place disponible.');
            } else {
                alert('Réservation effectuée avec succès !');
            }
        }

        // Initialisation de l'affichage
        genererPlan();
    </script>
</body>
</html>