
const API_BASE = "/api";

let currentFilters = {
    hostname: "",
    status: "",
    risk_level: "",
    equipment_type: ""
};


// ============================================================
// UTILITIES
// ============================================================

function formatNumber(value, decimals = 0) {

    if (value === null || value === undefined) {
        return "--";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
        return "--";
    }

    return number.toFixed(decimals);
}


function statusBadge(status) {

    if (!status) {
        return `<span class="badge">--</span>`;
    }

    const normalized =
        String(status).toUpperCase();

    let className = "badge-ok";

    if (normalized === "WARNING") {
        className = "badge-warning";
    }

    if (normalized === "CRITICAL") {
        className = "badge-critical";
    }

    return `
        <span class="badge ${className}">
            ${normalized}
        </span>
    `;
}


function riskBadge(risk) {

    if (!risk) {
        return `<span class="badge">--</span>`;
    }

    const normalized =
        String(risk).toUpperCase();

    let className = "badge-low";

    if (normalized === "MEDIUM") {
        className = "badge-medium";
    }

    if (normalized === "HIGH") {
        className = "badge-high";
    }

    return `
        <span class="badge ${className}">
            ${normalized}
        </span>
    `;
}


function formatTimestamp(timestamp) {

    if (!timestamp) {
        return "--";
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
        return timestamp;
    }

    return date.toLocaleString("fr-FR", {
        day: "2-digit",
        month: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}


// ============================================================
// FILTER QUERY
// ============================================================

function buildQuery() {

    const params =
        new URLSearchParams();

    if (currentFilters.hostname) {

        params.set(
            "hostname",
            currentFilters.hostname
        );
    }

    if (currentFilters.status) {

        params.set(
            "status",
            currentFilters.status
        );
    }

    if (currentFilters.risk_level) {

        params.set(
            "risk_level",
            currentFilters.risk_level
        );
    }

    const query =
        params.toString();

    return query
        ? `?${query}`
        : "";
}


// ============================================================
// GET SECTIONS
// ============================================================

function getEquipmentSections() {

    return {

        servers:
            document
                .getElementById("servers-table")
                .closest(".equipment-panel"),

        ups:
            document
                .getElementById("ups-table")
                .closest(".equipment-panel"),

        cooling:
            document
                .getElementById("cooling-table")
                .closest(".equipment-panel")
    };
}


// ============================================================
// SHOW / HIDE EQUIPMENT SECTIONS
// ============================================================

function showAllEquipmentSections() {

    const sections =
        getEquipmentSections();

    sections.servers.style.display = "";
    sections.ups.style.display = "";
    sections.cooling.style.display = "";
}


function showOnlyEquipment(type) {

    const sections =
        getEquipmentSections();

    sections.servers.style.display =
        type === "servers"
            ? ""
            : "none";

    sections.ups.style.display =
        type === "ups"
            ? ""
            : "none";

    sections.cooling.style.display =
        type === "cooling"
            ? ""
            : "none";
}


// ============================================================
// DASHBOARD STATISTICS
// ============================================================

async function loadDashboardStatistics() {

    try {

        const response =
            await fetch(
                `${API_BASE}/dashboard/statistics`
            );

        if (!response.ok) {

            throw new Error(
                "Erreur API statistiques"
            );
        }

        const data =
            await response.json();

        const servers =
            data.servers || {};

        const ups =
            data.ups || {};

        const cooling =
            data.cooling || {};


        const total =
            Number(servers.total || 0) +
            Number(ups.total || 0) +
            Number(cooling.total || 0);


        const ok =
            Number(servers.ok || 0) +
            Number(ups.ok || 0) +
            Number(cooling.ok || 0);


        const warning =
            Number(servers.warning || 0) +
            Number(ups.warning || 0) +
            Number(cooling.warning || 0);


        const critical =
            Number(servers.critical || 0) +
            Number(ups.critical || 0) +
            Number(cooling.critical || 0);


        document.getElementById(
            "total-equipment"
        ).textContent = total;


        document.getElementById(
            "total-ok"
        ).textContent = ok;


        document.getElementById(
            "total-warning"
        ).textContent = warning;


        document.getElementById(
            "total-critical"
        ).textContent = critical;


        document.getElementById(
            "total-anomalies"
        ).textContent =
            data.total_anomalies || 0;

    }

    catch (error) {

        console.error(
            "Erreur statistiques:",
            error
        );
    }
}


// ============================================================
// SERVERS
// ============================================================

async function loadServers() {

    const table =
        document.getElementById(
            "servers-table"
        );

    try {

        const response =
            await fetch(
                `${API_BASE}/equipment/servers${buildQuery()}`
            );

        if (!response.ok) {

            throw new Error(
                "Erreur serveurs"
            );
        }

        const data =
            await response.json();


        document.getElementById(
            "server-count"
        ).textContent =
            data.length;


        if (!data.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="9"
                        class="loading">

                        Aucun serveur trouvé.

                    </td>
                </tr>
            `;

            return;
        }


        table.innerHTML =
            data.map(server => `

                <tr>

                    <td>
                        <strong>
                            ${server.hostname || "--"}
                        </strong>
                    </td>

                    <td>
                        ${formatNumber(server.cpu)} %
                    </td>

                    <td>
                        ${formatNumber(server.ram)} %
                    </td>

                    <td>
                        ${formatNumber(server.temperature)} °C
                    </td>

                    <td>
                        ${formatNumber(server.power)} W
                    </td>

                    <td>
                        ${statusBadge(server.status)}
                    </td>

                    <td>
                        ${riskBadge(server.risk_level)}
                    </td>

                    <td>
                        ${server.anomaly_count || 0}
                    </td>

                    <td>
                        ${formatTimestamp(server.timestamp)}
                    </td>

                </tr>

            `).join("");

    }

    catch (error) {

        console.error(
            "Erreur serveurs:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="9"
                    class="loading">

                    Impossible de charger les serveurs.

                </td>
            </tr>
        `;
    }
}


// ============================================================
// UPS
// ============================================================

async function loadUPS() {

    const table =
        document.getElementById(
            "ups-table"
        );

    try {

        const response =
            await fetch(
                `${API_BASE}/equipment/ups${buildQuery()}`
            );

        if (!response.ok) {

            throw new Error(
                "Erreur UPS"
            );
        }

        const data =
            await response.json();


        document.getElementById(
            "ups-count"
        ).textContent =
            data.length;


        if (!data.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="9"
                        class="loading">

                        Aucun UPS trouvé.

                    </td>
                </tr>
            `;

            return;
        }


        table.innerHTML =
            data.map(ups => `

                <tr>

                    <td>
                        <strong>
                            ${ups.hostname || "--"}
                        </strong>
                    </td>

                    <td>
                        ${formatNumber(
                            ups.battery_level
                        )} %
                    </td>

                    <td>
                        ${formatNumber(
                            ups.runtime
                        )} min
                    </td>

                    <td>
                        ${formatNumber(
                            ups.load
                        )} %
                    </td>

                    <td>
                        ${formatNumber(
                            ups.temperature
                        )} °C
                    </td>

                    <td>
                        ${formatNumber(
                            ups.power
                        )} W
                    </td>

                    <td>
                        ${statusBadge(
                            ups.status
                        )}
                    </td>

                    <td>
                        ${riskBadge(
                            ups.risk_level
                        )}
                    </td>

                    <td>
                        ${ups.anomaly_count || 0}
                    </td>

                </tr>

            `).join("");

    }

    catch (error) {

        console.error(
            "Erreur UPS:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="9"
                    class="loading">

                    Impossible de charger les UPS.

                </td>
            </tr>
        `;
    }
}


// ============================================================
// COOLING
// ============================================================

async function loadCooling() {

    const table =
        document.getElementById(
            "cooling-table"
        );

    try {

        const response =
            await fetch(
                `${API_BASE}/equipment/cooling${buildQuery()}`
            );

        if (!response.ok) {

            throw new Error(
                "Erreur cooling"
            );
        }

        const data =
            await response.json();


        document.getElementById(
            "cooling-count"
        ).textContent =
            data.length;


        if (!data.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="9"
                        class="loading">

                        Aucun équipement cooling trouvé.

                    </td>
                </tr>
            `;

            return;
        }


        table.innerHTML =
            data.map(cooling => `

                <tr>

                    <td>
                        <strong>
                            ${cooling.hostname || "--"}
                        </strong>
                    </td>

                    <td>
                        ${formatNumber(
                            cooling.supply_temperature
                        )} °C
                    </td>

                    <td>
                        ${formatNumber(
                            cooling.return_temperature
                        )} °C
                    </td>

                    <td>
                        ${formatNumber(
                            cooling.humidity
                        )} %
                    </td>

                    <td>
                        ${formatNumber(
                            cooling.fan_speed
                        )} RPM
                    </td>

                    <td>
                        ${formatNumber(
                            cooling.power
                        )} W
                    </td>

                    <td>
                        ${formatNumber(
                            cooling.pressure
                        )}
                    </td>

                    <td>
                        ${statusBadge(
                            cooling.status
                        )}
                    </td>

                    <td>
                        ${cooling.anomaly_count || 0}
                    </td>

                </tr>

            `).join("");

    }

    catch (error) {

        console.error(
            "Erreur cooling:",
            error
        );

        table.innerHTML = `
            <tr>
                <td colspan="9"
                    class="loading">

                    Impossible de charger le cooling.

                </td>
            </tr>
        `;
    }
}


// ============================================================
// ANOMALIES
// ============================================================

async function loadAnomalies() {

    const serverTable =
        document.getElementById(
            "servers-table"
        );

    const upsTable =
        document.getElementById(
            "ups-table"
        );

    const coolingTable =
        document.getElementById(
            "cooling-table"
        );


    try {

        const [
            serversResponse,
            upsResponse,
            coolingResponse
        ] = await Promise.all([

            fetch(
                `${API_BASE}/equipment/servers${buildQuery()}`
            ),

            fetch(
                `${API_BASE}/equipment/ups${buildQuery()}`
            ),

            fetch(
                `${API_BASE}/equipment/cooling${buildQuery()}`
            )

        ]);


        if (
            !serversResponse.ok ||
            !upsResponse.ok ||
            !coolingResponse.ok
        ) {

            throw new Error(
                "Erreur chargement anomalies"
            );
        }


        const servers =
            await serversResponse.json();

        const ups =
            await upsResponse.json();

        const cooling =
            await coolingResponse.json();


        const anomalousServers =
            servers.filter(
                item =>
                    Number(
                        item.anomaly_count || 0
                    ) > 0
            );


        const anomalousUPS =
            ups.filter(
                item =>
                    Number(
                        item.anomaly_count || 0
                    ) > 0
            );


        const anomalousCooling =
            cooling.filter(
                item =>
                    Number(
                        item.anomaly_count || 0
                    ) > 0
            );


        // ====================================================
        // SERVERS
        // ====================================================

        if (!anomalousServers.length) {

            serverTable.innerHTML = `
                <tr>
                    <td colspan="9"
                        class="loading">

                        Aucune anomalie serveur.

                    </td>
                </tr>
            `;

        }

        else {

            serverTable.innerHTML =
                anomalousServers.map(server => `

                    <tr>

                        <td>
                            <strong>
                                ${server.hostname || "--"}
                            </strong>
                        </td>

                        <td>
                            ${formatNumber(
                                server.cpu
                            )} %
                        </td>

                        <td>
                            ${formatNumber(
                                server.ram
                            )} %
                        </td>

                        <td>
                            ${formatNumber(
                                server.temperature
                            )} °C
                        </td>

                        <td>
                            ${formatNumber(
                                server.power
                            )} W
                        </td>

                        <td>
                            ${statusBadge(
                                server.status
                            )}
                        </td>

                        <td>
                            ${riskBadge(
                                server.risk_level
                            )}
                        </td>

                        <td>
                            ${server.anomaly_count || 0}
                        </td>

                        <td>
                            ${formatTimestamp(
                                server.timestamp
                            )}
                        </td>

                    </tr>

                `).join("");
        }


        // ====================================================
        // UPS
        // ====================================================

        if (!anomalousUPS.length) {

            upsTable.innerHTML = `
                <tr>
                    <td colspan="9"
                        class="loading">

                        Aucune anomalie UPS.

                    </td>
                </tr>
            `;

        }

        else {

            upsTable.innerHTML =
                anomalousUPS.map(ups => `

                    <tr>

                        <td>
                            <strong>
                                ${ups.hostname || "--"}
                            </strong>
                        </td>

                        <td>
                            ${formatNumber(
                                ups.battery_level
                            )} %
                        </td>

                        <td>
                            ${formatNumber(
                                ups.runtime
                            )} min
                        </td>

                        <td>
                            ${formatNumber(
                                ups.load
                            )} %
                        </td>

                        <td>
                            ${formatNumber(
                                ups.temperature
                            )} °C
                        </td>

                        <td>
                            ${formatNumber(
                                ups.power
                            )} W
                        </td>

                        <td>
                            ${statusBadge(
                                ups.status
                            )}
                        </td>

                        <td>
                            ${riskBadge(
                                ups.risk_level
                            )}
                        </td>

                        <td>
                            ${ups.anomaly_count || 0}
                        </td>

                    </tr>

                `).join("");
        }


        // ====================================================
        // COOLING
        // ====================================================

        if (!anomalousCooling.length) {

            coolingTable.innerHTML = `
                <tr>
                    <td colspan="9"
                        class="loading">

                        Aucune anomalie cooling.

                    </td>
                </tr>
            `;

        }

        else {

            coolingTable.innerHTML =
                anomalousCooling.map(
                    cooling => `

                    <tr>

                        <td>
                            <strong>
                                ${cooling.hostname || "--"}
                            </strong>
                        </td>

                        <td>
                            ${formatNumber(
                                cooling.supply_temperature
                            )} °C
                        </td>

                        <td>
                            ${formatNumber(
                                cooling.return_temperature
                            )} °C
                        </td>

                        <td>
                            ${formatNumber(
                                cooling.humidity
                            )} %
                        </td>

                        <td>
                            ${formatNumber(
                                cooling.fan_speed
                            )} RPM
                        </td>

                        <td>
                            ${formatNumber(
                                cooling.power
                            )} W
                        </td>

                        <td>
                            ${formatNumber(
                                cooling.pressure
                            )}
                        </td>

                        <td>
                            ${statusBadge(
                                cooling.status
                            )}
                        </td>

                        <td>
                            ${cooling.anomaly_count || 0}
                        </td>

                    </tr>

                `).join("");
        }

    }

    catch (error) {

        console.error(
            "Erreur anomalies:",
            error
        );
    }
}


// ============================================================
// LOAD DASHBOARD
// ============================================================

async function loadDashboard() {

    await loadDashboardStatistics();


    const type =
        currentFilters.equipment_type;


    if (type === "servers") {

        showOnlyEquipment("servers");

        await loadServers();

    }

    else if (type === "ups") {

        showOnlyEquipment("ups");

        await loadUPS();

    }

    else if (type === "cooling") {

        showOnlyEquipment("cooling");

        await loadCooling();

    }

    else {

        showAllEquipmentSections();

        await Promise.all([
            loadServers(),
            loadUPS(),
            loadCooling()
        ]);
    }
}


// ============================================================
// FILTERS
// ============================================================

function applyFilters() {

    currentFilters.hostname =
        document
            .getElementById(
                "hostname-filter"
            )
            .value
            .trim();


    currentFilters.status =
        document.getElementById(
            "status-filter"
        ).value;


    currentFilters.risk_level =
        document.getElementById(
            "risk-filter"
        ).value;


    currentFilters.equipment_type =
        document.getElementById(
            "equipment-type"
        ).value;


    const type =
        currentFilters.equipment_type;


    if (type === "servers") {

        showOnlyEquipment("servers");

        loadServers();

    }

    else if (type === "ups") {

        showOnlyEquipment("ups");

        loadUPS();

    }

    else if (type === "cooling") {

        showOnlyEquipment("cooling");

        loadCooling();

    }

    else {

        showAllEquipmentSections();

        loadServers();
        loadUPS();
        loadCooling();
    }
}


// ============================================================
// CLEAR FILTERS
// ============================================================

function clearFilters() {

    document.getElementById(
        "hostname-filter"
    ).value = "";


    document.getElementById(
        "status-filter"
    ).value = "";


    document.getElementById(
        "risk-filter"
    ).value = "";


    document.getElementById(
        "equipment-type"
    ).value = "";


    currentFilters = {

        hostname: "",
        status: "",
        risk_level: "",
        equipment_type: ""
    };


    showAllEquipmentSections();

    loadDashboard();
}


// ============================================================
// SIDEBAR NAVIGATION
// ============================================================

// ============================================================
// SIDEBAR NAVIGATION
// ============================================================

function showSection(section) {

    const serverTable =
        document.getElementById("servers-table");

    const upsTable =
        document.getElementById("ups-table");

    const coolingTable =
        document.getElementById("cooling-table");

    const aiSection =
        document.getElementById("ai-section");


    const serverSection =
        serverTable.closest(".equipment-panel");

    const upsSection =
        upsTable.closest(".equipment-panel");

    const coolingSection =
        coolingTable.closest(".equipment-panel");


    // ========================================================
    // CACHER AI PAR DÉFAUT
    // ========================================================

    if (aiSection) {
        aiSection.style.display = "none";
    }


    // ========================================================
    // DASHBOARD
    // ========================================================

    if (section === "dashboard") {

        serverSection.style.display = "";
        upsSection.style.display = "";
        coolingSection.style.display = "";

        currentFilters.equipment_type = "";

        const equipmentType =
            document.getElementById("equipment-type");

        if (equipmentType) {
            equipmentType.value = "all";
        }

        loadDashboard();
    }


    // ========================================================
    // SERVERS
    // ========================================================

    else if (section === "servers") {

        serverSection.style.display = "";
        upsSection.style.display = "none";
        coolingSection.style.display = "none";

        currentFilters.equipment_type = "servers";

        loadServers();
    }


    // ========================================================
    // UPS
    // ========================================================

    else if (section === "ups") {

        serverSection.style.display = "none";
        upsSection.style.display = "";
        coolingSection.style.display = "none";

        currentFilters.equipment_type = "ups";

        loadUPS();
    }


    // ========================================================
    // COOLING
    // ========================================================

    else if (section === "cooling") {

        serverSection.style.display = "none";
        upsSection.style.display = "none";
        coolingSection.style.display = "";

        currentFilters.equipment_type = "cooling";

        loadCooling();
    }


    // ========================================================
    // ANOMALIES
    // ========================================================

    else if (section === "anomalies") {

        serverSection.style.display = "";
        upsSection.style.display = "";
        coolingSection.style.display = "";

        currentFilters.equipment_type = "";

        loadServers();
        loadUPS();
        loadCooling();
    }


    // ========================================================
    // AI ASSISTANT
    // ========================================================

    else if (section === "ai") {

        serverSection.style.display = "none";
        upsSection.style.display = "none";
        coolingSection.style.display = "none";

        currentFilters.equipment_type = "";

        if (aiSection) {
            aiSection.style.display = "";
        }
    }


    // ========================================================
    // SIDEBAR ACTIVE ITEM
    // ========================================================

    document
        .querySelectorAll(".nav-item[data-section]")
        .forEach(item => {

            item.classList.remove("active");

            if (
                item.dataset.section === section
            ) {

                item.classList.add("active");

            }

        });

}

// ============================================================
// SIDEBAR CLICK EVENTS
// ============================================================

function initializeSidebar() {

    document
        .querySelectorAll(
            ".nav-item[data-section]"
        )
        .forEach(item => {

            item.addEventListener(
                "click",
                function(event) {

                    event.preventDefault();


                    const section =
                        this.dataset.section;


                    window.location.hash =
                        section;


                    showSection(
                        section
                    );
                }
            );
        });
}


// ============================================================
// HASH CHANGE
// ============================================================

window.addEventListener(
    "hashchange",
    () => {

        const section =
            window.location.hash
                .replace("#", "") ||
            "dashboard";


        showSection(
            section
        );
    }
);


// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeSidebar();


        const section =
            window.location.hash
                .replace("#", "") ||
            "dashboard";


        showSection(
            section
        );


        // Actualisation automatique
        // toutes les 30 secondes.

        setInterval(
            () => {

                const currentSection =
                    window.location.hash
                        .replace("#", "") ||
                    "dashboard";


                if (
                    currentSection ===
                    "dashboard"
                ) {

                    loadDashboard();

                }

                else if (
                    currentSection ===
                    "servers"
                ) {

                    loadServers();

                }

                else if (
                    currentSection ===
                    "ups"
                ) {

                    loadUPS();

                }

                else if (
                    currentSection ===
                    "cooling"
                ) {

                    loadCooling();

                }

                else if (
                    currentSection ===
                    "anomalies"
                ) {

                    loadAnomalies();

                }

            },
            30000
        );
    }
);
// ============================================================
// AI ASSISTANT
// ============================================================

async function sendAIMessage() {

    const input =
        document.getElementById("ai-input");

    const messages =
        document.getElementById("ai-messages");

    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    // --------------------------------------------------------
    // MESSAGE UTILISATEUR
    // --------------------------------------------------------

    messages.innerHTML += `

        <div class="ai-message user">

            <div class="ai-bubble">

                ${question}

            </div>

        </div>

    `;


    input.value = "";


    // --------------------------------------------------------
    // INDICATEUR
    // --------------------------------------------------------

    messages.innerHTML += `

        <div id="ai-loading"
             class="ai-message assistant">

            <div class="ai-avatar">
                ✦
            </div>

            <div class="ai-bubble">

                Analyse des données...

            </div>

        </div>

    `;


    messages.scrollTop =
        messages.scrollHeight;


    try {

        const response = await fetch(
            `${API_BASE}/ai/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data =
            await response.json();


        const loading =
            document.getElementById(
                "ai-loading"
            );


        if (loading) {
            loading.remove();
        }


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Erreur AI"
            );

        }


        messages.innerHTML += `

            <div class="ai-message assistant">

                <div class="ai-avatar">
                    ✦
                </div>

                <div class="ai-bubble">

                    ${data.answer}

                </div>

            </div>

        `;


    }

    catch (error) {

        const loading =
            document.getElementById(
                "ai-loading"
            );

        if (loading) {
            loading.remove();
        }


        messages.innerHTML += `

            <div class="ai-message assistant">

                <div class="ai-avatar">
                    !
                </div>

                <div class="ai-bubble">

                    Impossible de contacter
                    l'assistant AI.

                    <br>

                    ${error.message}

                </div>

            </div>

        `;

        console.error(
            "AI error:",
            error
        );

    }


    messages.scrollTop =
        messages.scrollHeight;
}
