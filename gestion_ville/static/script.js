const API_BASE_URL = "/api";

const villeTableBody = document.getElementById("villeTableBody");
const villeCount = document.getElementById("villeCount");

const formModal = document.getElementById("formModal");
const showFormBtn = document.getElementById("showFormBtn");
const closeFormBtn = document.getElementById("closeFormBtn");
const resetBtn = document.getElementById("resetBtn");

const villeForm = document.getElementById("villeForm");
const villeIdInput = document.getElementById("villeId");
const nomVilleInput = document.getElementById("nom_ville");
const codeVilleInput = document.getElementById("code_ville");
const regionInput = document.getElementById("region");
const paysInput = document.getElementById("pays");
const statutInput = document.getElementById("statut");

const formTitle = document.getElementById("formTitle");
const formSubtitle = document.getElementById("formSubtitle");
const messageBox = document.getElementById("message");

document.addEventListener("DOMContentLoaded", () => {
    initialiserEvenements();
    chargerVilles();
});

function initialiserEvenements() {
    showFormBtn.addEventListener("click", ouvrirFormulaireAjout);
    closeFormBtn.addEventListener("click", fermerModal);
    resetBtn.addEventListener("click", annulerFormulaire);

    formModal.addEventListener("click", (event) => {
        if (event.target === formModal) {
            fermerModal();
        }
    });

    villeForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await enregistrerVille();
    });
}

function ouvrirModal() {
    formModal.classList.remove("hidden");
}

function fermerModal() {
    formModal.classList.add("hidden");
    clearMessage();
}

function ouvrirFormulaireAjout() {
    resetFormulaire();
    ouvrirModal();
}

function annulerFormulaire() {
    resetFormulaire();
    fermerModal();
}

function resetFormulaire() {
    villeForm.reset();
    villeIdInput.value = "";
    paysInput.value = "Mauritanie";
    formTitle.textContent = "Ajouter une ville";
    formSubtitle.textContent = "Remplissez le formulaire pour enregistrer une nouvelle ville.";
    clearMessage();
}

function remplirFormulaireModification(ville) {
    villeIdInput.value = ville.id;
    nomVilleInput.value = ville.nom_ville || "";
    codeVilleInput.value = ville.code_ville || "";
    regionInput.value = ville.region || "";
    paysInput.value = ville.pays || "";
    statutInput.value = ville.statut || "";

    formTitle.textContent = "Modifier une ville";
    formSubtitle.textContent = "Modifiez les informations de la ville sélectionnée.";
    clearMessage();
    ouvrirModal();
}

function afficherMessage(message, type = "success") {
    messageBox.textContent = message;
    messageBox.style.color = type === "success" ? "#15803d" : "#dc2626";
}

function clearMessage() {
    messageBox.textContent = "";
}

function escapeHtml(value) {
    if (value === null || value === undefined) return "";
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function genererBadgeStatut(statut) {
    const s = (statut || "").toLowerCase();
    return s === "active"
        ? '<span class="badge-active">Active</span>'
        : '<span class="badge-inactive">Inactive</span>';
}

async function chargerVilles() {
    try {
        villeTableBody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-row">Chargement des données...</td>
            </tr>
        `;

        const response = await fetch(`${API_BASE_URL}/lire/villes`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur lors du chargement des villes.");
        }

        if (!Array.isArray(data) || data.length === 0) {
            villeCount.textContent = "0";
            villeTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="empty-row">Aucune donnée à afficher pour le moment.</td>
                </tr>
            `;
            return;
        }

        villeCount.textContent = data.length;
        villeTableBody.innerHTML = "";

        data.forEach((ville) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${escapeHtml(ville.id)}</td>
                <td>${escapeHtml(ville.nom_ville)}</td>
                <td>${escapeHtml(ville.code_ville)}</td>
                <td>${escapeHtml(ville.region)}</td>
                <td>${escapeHtml(ville.pays)}</td>
                <td>${genererBadgeStatut(ville.statut)}</td>
                <td>
                    <button type="button" class="btn-edit" onclick="chargerVillePourEdition(${ville.id})">
                        <i class="fa-solid fa-pen"></i> Modifier
                    </button>
                    <button type="button" class="btn-delete" onclick="supprimerVille(${ville.id})">
                        <i class="fa-solid fa-trash"></i> Supprimer
                    </button>
                </td>
            `;
            villeTableBody.appendChild(row);
        });
    } catch (error) {
        villeCount.textContent = "0";
        villeTableBody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-row">Erreur de chargement des données.</td>
            </tr>
        `;
        alert(error.message);
        console.error(error);
    }
}

async function chargerVillePourEdition(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/lire/ville/${id}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Impossible de récupérer cette ville.");
        }

        remplirFormulaireModification(data);
    } catch (error) {
        alert(error.message);
    }
}

function recupererDonneesFormulaire() {
    return {
        nom_ville: nomVilleInput.value.trim(),
        code_ville: codeVilleInput.value.trim(),
        region: regionInput.value.trim(),
        pays: paysInput.value.trim(),
        statut: statutInput.value.trim()
    };
}

function validerFormulaire(payload) {
    if (!payload.nom_ville || !payload.code_ville || !payload.region || !payload.pays || !payload.statut) {
        afficherMessage("Tous les champs sont obligatoires.", "error");
        return false;
    }
    return true;
}

async function enregistrerVille() {
    const id = villeIdInput.value.trim();
    const payload = recupererDonneesFormulaire();

    clearMessage();

    if (!validerFormulaire(payload)) {
        return;
    }

    try {
        let url = `${API_BASE_URL}/ajouter/ville`;
        let method = "POST";

        if (id) {
            url = `${API_BASE_URL}/modifier/ville/${id}`;
            method = "PUT";
        }

        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur lors de l'enregistrement.");
        }

        await chargerVilles();
        resetFormulaire();
        fermerModal();
        alert(data.message || "Opération réussie.");
    } catch (error) {
        afficherMessage(error.message, "error");
    }
}

async function supprimerVille(id) {
    const confirmation = confirm("Voulez-vous vraiment supprimer cette ville ?");

    if (!confirmation) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/supprimer/ville/${id}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur lors de la suppression.");
        }

        await chargerVilles();
        alert(data.message || "Ville supprimée avec succès.");
    } catch (error) {
        alert("Erreur suppression : " + error.message);
        console.error(error);
    }
}

window.chargerVillePourEdition = chargerVillePourEdition;
window.supprimerVille = supprimerVille;