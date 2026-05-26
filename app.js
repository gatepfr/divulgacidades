// Lógica da Aplicação (app.js)

// Mapeamento de Siglas de Estados para Nomes Completos para melhor experiência de busca
const NOMES_ESTADOS = {
  "AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá", "BA": "Bahia",
  "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
  "MA": "Maranhão", "MG": "Minas Gerais", "MS": "Mato Grosso do Sul", "MT": "Mato Grosso",
  "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco", "PI": "Piauí", "PR": "Paraná",
  "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RO": "Rondônia", "RR": "Roraima",
  "RS": "Rio Grande do Sul", "SC": "Santa Catarina", "SE": "Sergipe", "SP": "São Paulo",
  "TO": "Tocantins"
};

// Estado da Aplicação
let appState = {
  selectedState: null,
  selectedCity: null,
  cityData: null,
  activeTab: "prefeito",
  searchQuery: ""
};

// Elementos DOM
const stateInput = document.getElementById("state-input");
const stateDropdown = document.getElementById("state-dropdown");
const cityInput = document.getElementById("city-input");
const cityDropdown = document.getElementById("city-dropdown");
const cityComboboxContainer = document.getElementById("city-combobox-container");

const emptyStateView = document.getElementById("empty-state-view");
const dashboardView = document.getElementById("dashboard-view");

const summaryUfFlag = document.getElementById("summary-uf-flag");
const summaryCityTitle = document.getElementById("summary-city-title");
const summaryCityDetails = document.getElementById("summary-city-details");

const candidateSearch = document.getElementById("candidate-search");
const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanes = document.querySelectorAll(".tab-pane");

// Elementos do Modal
const candidateModal = document.getElementById("candidate-modal");
const modalCloseBtn = document.getElementById("modal-close-btn");
const modalBtnConfirm = document.getElementById("modal-btn-confirm");
const modalAvatarPlaceholder = document.getElementById("modal-avatar-placeholder");
const modalBadgeCargo = document.getElementById("modal-badge-cargo");
const modalCandidateName = document.getElementById("modal-candidate-name");
const modalCandidateParty = document.getElementById("modal-candidate-party");
const modalCandidatePartyNumber = document.getElementById("modal-candidate-party-number");
const modalCandidatePartyName = document.getElementById("modal-candidate-party-name");
const modalStatVotes = document.getElementById("modal-stat-votes");
const modalStatPercent = document.getElementById("modal-stat-percent");
const modalStatSituation = document.getElementById("modal-stat-situation");
const modalDetailNumber = document.getElementById("modal-detail-number");
const modalDetailColigacao = document.getElementById("modal-detail-coligacao");
const modalRowColigacao = document.getElementById("modal-row-coligacao");
const modalDetailJurisdiction = document.getElementById("modal-detail-jurisdiction");
const modalDetailYear = document.getElementById("modal-detail-year");
const modalProgressBar = document.getElementById("modal-progress-bar");

// --- INICIALIZAÇÃO E EVENTOS ---

document.addEventListener("DOMContentLoaded", () => {
  setupComboboxes();
  setupTabs();
  setupSearch();
  setupModal();
});

// Atalho da página inicial (Showcases com dados reais)
window.selectShowcase = (uf, cidade) => {
  selectState(uf);
  stateInput.value = `${uf} - ${NOMES_ESTADOS[uf]}`;
  
  setTimeout(() => {
    selectCity(cidade);
    cityInput.value = cidade;
  }, 100);
};

// --- CUSTOM COMBOBOXES (AUTOCOMPLETAR) ---

function setupComboboxes() {
  // --- ESTADOS ---
  // Abre ao focar/clicar
  stateInput.addEventListener("focus", () => {
    renderStatesDropdown();
    stateDropdown.classList.add("show");
  });

  // Filtra ao digitar
  stateInput.addEventListener("input", (e) => {
    renderStatesDropdown(e.target.value);
    stateDropdown.classList.add("show");
  });

  // Fecha ao clicar fora
  document.addEventListener("click", (e) => {
    if (!stateInput.parentNode.contains(e.target) && !stateDropdown.contains(e.target)) {
      stateDropdown.classList.remove("show");
    }
  });

  // --- CIDADES ---
  // Abre ao focar/clicar
  cityInput.addEventListener("focus", () => {
    if (appState.selectedState) {
      renderCitiesDropdown();
      cityDropdown.classList.add("show");
    }
  });

  // Filtra ao digitar
  cityInput.addEventListener("input", (e) => {
    if (appState.selectedState) {
      renderCitiesDropdown(e.target.value);
      cityDropdown.classList.add("show");
    }
  });

  // Aceita cidade customizada ao pressionar Enter
  cityInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && cityInput.value.trim() !== "") {
      const typedCity = cityInput.value.trim();
      selectCity(typedCity);
      cityDropdown.classList.remove("show");
      cityInput.blur();
    }
  });

  // Fecha ao clicar fora
  document.addEventListener("click", (e) => {
    if (!cityInput.parentNode.contains(e.target) && !cityDropdown.contains(e.target)) {
      cityDropdown.classList.remove("show");
    }
  });
}

// Renderiza lista de estados
function renderStatesDropdown(filterText = "") {
  stateDropdown.innerHTML = "";
  const filter = filterText.toLowerCase().trim();
  
  const stateCodes = Object.keys(NOMES_ESTADOS);
  const filteredCodes = stateCodes.filter(code => {
    const nome = NOMES_ESTADOS[code].toLowerCase();
    const sigla = code.toLowerCase();
    return nome.includes(filter) || sigla.includes(filter);
  });

  if (filteredCodes.length === 0) {
    const emptyItem = document.createElement("div");
    emptyItem.className = "combobox-item";
    emptyItem.style.color = "var(--text-muted)";
    emptyItem.innerText = "Nenhum estado encontrado";
    stateDropdown.appendChild(emptyItem);
    return;
  }

  filteredCodes.forEach(code => {
    const item = document.createElement("div");
    item.className = "combobox-item";
    item.innerText = `${code} - ${NOMES_ESTADOS[code]}`;
    item.addEventListener("click", () => {
      selectState(code);
      stateInput.value = `${code} - ${NOMES_ESTADOS[code]}`;
      stateDropdown.classList.remove("show");
    });
    stateDropdown.appendChild(item);
  });
}

// Renderiza lista de cidades do estado ativo
function renderCitiesDropdown(filterText = "") {
  cityDropdown.innerHTML = "";
  const filter = filterText.toLowerCase().trim();
  
  const cities = window.ESTADOS_CIDADES[appState.selectedState] || [];
  let filteredCities = cities.filter(city => city.toLowerCase().includes(filter));

  // Opção para criar uma cidade customizada gerada por semente se não estiver na lista predefinida
  if (filterText && !filteredCities.some(c => c.toLowerCase() === filter)) {
    const customItem = document.createElement("div");
    customItem.className = "combobox-item highlighted";
    customItem.innerHTML = `✨ Usar: <strong>"${filterText}"</strong> <span style="font-size:0.75rem;opacity:0.6;margin-left:0.5rem">(Gerar dados da cidade)</span>`;
    customItem.addEventListener("click", () => {
      selectCity(filterText);
      cityInput.value = filterText;
      cityDropdown.classList.remove("show");
    });
    cityDropdown.appendChild(customItem);
  }

  filteredCities.forEach(city => {
    const item = document.createElement("div");
    item.className = "combobox-item";
    item.innerText = city;
    item.addEventListener("click", () => {
      selectCity(city);
      cityInput.value = city;
      cityDropdown.classList.remove("show");
    });
    cityDropdown.appendChild(item);
  });

  if (filteredCities.length === 0 && !filterText) {
    const emptyItem = document.createElement("div");
    emptyItem.className = "combobox-item";
    emptyItem.innerText = "Nenhuma cidade padrão. Digite o nome.";
    cityDropdown.appendChild(emptyItem);
  }
}

// Manipula seleção de Estado
function selectState(ufCode) {
  appState.selectedState = ufCode;
  appState.selectedCity = null;
  appState.cityData = null;
  
  // Limpa e ativa campo de cidade
  cityInput.value = "";
  cityInput.placeholder = "Digite ou escolha a cidade...";
  cityInput.disabled = false;
  cityComboboxContainer.classList.remove("disabled");
  
  // Limpa visualizações de resultados
  emptyStateView.classList.remove("hidden");
  dashboardView.classList.add("hidden");
}

// Manipula seleção de Cidade
async function selectCity(cityName) {
  appState.selectedCity = cityName;
  
  // Obtém dados (tenta carregar dados reais da cidade primeiro)
  const cityData = await window.loadCityData(appState.selectedState, cityName);
  if (cityData) {
    appState.cityData = cityData;
  } else {
    // Fallback para gerador procedural determinístico
    appState.cityData = window.getElectionData(appState.selectedState, cityName);
  }
  
  // Trata abas e nomenclaturas específicas para o Distrito Federal
  updateDFTabs();
  
  // Exibe painel de resultados
  emptyStateView.classList.add("hidden");
  dashboardView.classList.remove("hidden");
  
  // Reseta filtros de busca
  candidateSearch.value = "";
  appState.searchQuery = "";
  
  // Renderiza Dashboard
  renderDashboard();
}

// Trata dinamicamente a exibição das abas e nomenclaturas para o Distrito Federal (DF)
function updateDFTabs() {
  const isDF = appState.selectedState === "DF";
  
  // Botões de aba
  const tabPref = document.querySelector('.tab-btn[data-tab="prefeito"]');
  const tabVer = document.querySelector('.tab-btn[data-tab="vereadores"]');
  const tabEst = document.querySelector('.tab-btn[data-tab="deputados-estaduais"]');
  
  // Títulos dos panes
  const paneEstTitle = document.querySelector('#pane-deputados-estaduais h3');
  const paneEstSubtitle = document.querySelector('#pane-deputados-estaduais .pane-subtitle');
  
  if (isDF) {
    if (tabPref) tabPref.style.display = "none";
    if (tabVer) tabVer.style.display = "none";
    if (tabEst) tabEst.innerText = "Dep. Distritais";
    if (paneEstTitle) paneEstTitle.innerText = "Deputados Distritais Mais Votados";
    if (paneEstSubtitle) paneEstSubtitle.innerText = "Top 7 candidatos com maior votação nominal no DF";
    
    // Se a aba ativa for prefeito ou vereadores (que não existem no DF), muda para senadores
    if (appState.activeTab === "prefeito" || appState.activeTab === "vereadores") {
      appState.activeTab = "senadores";
      // Atualiza os botões ativos
      tabButtons.forEach(btn => {
        if (btn.getAttribute("data-tab") === "senadores") {
          btn.classList.add("active");
          btn.setAttribute("aria-selected", "true");
        } else {
          btn.classList.remove("active");
          btn.setAttribute("aria-selected", "false");
        }
      });
      // Atualiza os panes ativos
      tabPanes.forEach(pane => {
        if (pane.id === "pane-senadores") {
          pane.classList.add("active");
        } else {
          pane.classList.remove("active");
        }
      });
    }
  } else {
    if (tabPref) tabPref.style.display = "block";
    if (tabVer) tabVer.style.display = "block";
    if (tabEst) tabEst.innerText = "Dep. Estaduais";
    if (paneEstTitle) paneEstTitle.innerText = "Deputados Estaduais Mais Votados";
    if (paneEstSubtitle) paneEstSubtitle.innerText = "Top 7 candidatos com maior votação nominal na cidade";
  }
}

// --- CONTROLES DE ABAS ---

function setupTabs() {
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Remove ativa de todos os botões
      tabButtons.forEach(b => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      
      // Ativa botão clicado
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      
      // Alterna panes
      const tabId = btn.getAttribute("data-tab");
      appState.activeTab = tabId;
      
      tabPanes.forEach(pane => {
        pane.classList.remove("active");
      });
      
      // Mapeamento correto de IDs de pane
      let targetPaneId = "pane-prefeito";
      if (tabId === "vereadores") targetPaneId = "pane-vereadores";
      else if (tabId === "senadores") targetPaneId = "pane-senadores";
      else if (tabId === "deputados-federais") targetPaneId = "pane-deputados-federais";
      else if (tabId === "deputados-estaduais") targetPaneId = "pane-deputados-estaduais";
      
      document.getElementById(targetPaneId).classList.add("active");
      
      // Reaplica filtro de busca se houver
      filterCandidatesOnTab();
    });
  });
}

// --- FILTRO DE BUSCA LOCAL ---

function setupSearch() {
  candidateSearch.addEventListener("input", (e) => {
    appState.searchQuery = e.target.value.toLowerCase().trim();
    filterCandidatesOnTab();
  });
}

function filterCandidatesOnTab() {
  const query = appState.searchQuery;
  const currentTab = appState.activeTab;
  
  if (currentTab === "prefeito") {
    // Para a aba de prefeito, apenas filtramos visualmente a chapa inteira
    const mayorCard = document.getElementById("mayor-card-main");
    const statsPanel = document.querySelector(".mayor-stats-panel");
    
    // Se os dados de prefeito forem nulos (ex: DF), ignora busca na aba
    if (!appState.cityData.prefeito) return;
    
    const matches = appState.cityData.prefeito.nome.toLowerCase().includes(query) || 
                    appState.cityData.prefeito.partido.toLowerCase().includes(query) ||
                    appState.cityData.prefeito.vice.toLowerCase().includes(query);
    
    if (matches) {
      if (mayorCard) mayorCard.style.opacity = "1";
      if (statsPanel) statsPanel.style.opacity = "1";
    } else {
      if (mayorCard) mayorCard.style.opacity = "0.2";
      if (statsPanel) statsPanel.style.opacity = "0.2";
    }
    return;
  }
  
  // Para outras abas, filtramos os cards da grid correspondente
  let gridId = "";
  if (currentTab === "vereadores") gridId = "grid-vereadores";
  else if (currentTab === "senadores") gridId = "grid-senadores";
  else if (currentTab === "deputados-federais") gridId = "grid-deputados-federais";
  else if (currentTab === "deputados-estaduais") gridId = "grid-deputados-estaduais";
  
  const grid = document.getElementById(gridId);
  const cards = grid.querySelectorAll(".candidate-card");
  let matchesCount = 0;
  
  cards.forEach(card => {
    const name = card.getAttribute("data-name").toLowerCase();
    const party = card.getAttribute("data-party").toLowerCase();
    
    if (name.includes(query) || party.includes(query)) {
      card.style.display = "flex";
      matchesCount++;
    } else {
      card.style.display = "none";
    }
  });

  // Placa de "nenhum resultado"
  let noResultsAlert = grid.querySelector(".no-results-alert");
  if (matchesCount === 0) {
    if (!noResultsAlert) {
      noResultsAlert = document.createElement("div");
      noResultsAlert.className = "no-results-alert";
      noResultsAlert.style.gridColumn = "1 / -1";
      noResultsAlert.style.padding = "2rem";
      noResultsAlert.style.textAlign = "center";
      noResultsAlert.style.color = "var(--text-muted)";
      noResultsAlert.innerText = "Nenhum candidato localizado com este filtro.";
      grid.appendChild(noResultsAlert);
    }
    noResultsAlert.style.display = "block";
  } else if (noResultsAlert) {
    noResultsAlert.style.display = "none";
  }
}

// --- RENDERIZADOR DO DASHBOARD ---

function renderDashboard() {
  const data = appState.cityData;
  const uf = appState.selectedState;
  const cidade = appState.selectedCity;
  
  // 1. Atualiza cabeçalho do resumo
  summaryUfFlag.innerText = uf;
  summaryCityTitle.innerText = `${cidade} - ${uf}`;
  
  let detailsText = "";
  if (uf === "DF") {
    // Info customizada para o Distrito Federal que não possui prefeituras
    detailsText = `Distrito Federal | População estimada: 2.817.068 hab | Dados de Votação (2022)`;
  } else if (data.populacao > 0) {
    const popFormatted = data.populacao.toLocaleString("pt-BR");
    const validFormatted = data.votosValidos.toLocaleString("pt-BR");
    detailsText = `População estimada: ${popFormatted} hab | Total de Votos Válidos: ${validFormatted}`;
  } else {
    detailsText = `Município de ${cidade} (${uf}) | Resultados das Eleições`;
  }
  summaryCityDetails.innerText = detailsText;

  // 2. Renderiza Prefeito & Vice (Aba principal)
  if (data.prefeito) {
    renderPrefeitoTab(data);
  }

  // 3. Renderiza Vereadores
  if (data.vereadores && data.vereadores.length > 0) {
    const eleitos = data.vereadores.filter(v => v.situacao && v.situacao.toLowerCase().startsWith("eleito"));
    let vereadoresToShow = data.vereadores;
    let labelText = "";
    
    if (eleitos.length > 0) {
      vereadoresToShow = eleitos;
      labelText = `${eleitos.length} vereadores eleitos`;
    } else {
      labelText = `${data.vereadores.length} vereadores no painel`;
    }
    
    renderCandidatesGrid("grid-vereadores", vereadoresToShow, "VEREADOR");
    document.getElementById("vereadores-count-label").innerText = labelText;
  }

  // 4. Renderiza Senadores (apenas top 3 mais votados)
  renderCandidatesGrid("grid-senadores", (data.senadores || []).slice(0, 3), "SENADOR");

  // 5. Renderiza Deputados Federais (apenas top 7 mais votados)
  renderCandidatesGrid("grid-deputados-federais", (data.deputadosFederais || []).slice(0, 7), "DEP. FEDERAL");

  // 6. Renderiza Deputados Estaduais (apenas top 7 mais votados)
  const cargoEstadual = uf === "DF" ? "DEP. ESTADUAL" : "DEP. ESTADUAL"; // Usado internamente para mapeamento de dados
  renderCandidatesGrid("grid-deputados-estaduais", (data.deputadosEstaduais || []).slice(0, 7), cargoEstadual);

}

// Renderiza a aba específica do prefeito
function renderPrefeitoTab(data) {
  const pref = data.prefeito;
  const uf = appState.selectedState;
  const ticketCard = document.getElementById("mayor-card-main");
  
  // Busca foto real pelo TSE CDN ou usa avatar como fallback imediato
  const photoUrl = window.getCandidatePhotoUrl(uf, pref.sqcand, 2024) || window.getCandidateAvatarUrl(pref.nome, pref.partido);
  const photoViceUrl = window.getCandidatePhotoUrl(uf, pref.sqcandVice, 2024) || window.getCandidateAvatarUrl(pref.vice, pref.partidoVice);
  
  const votosFormatted = pref.votos.toLocaleString("pt-BR");

  ticketCard.innerHTML = `
    <!-- Prefeito Principal -->
    <div class="mayor-main-row">
      <div class="mayor-photo-container">
        <img src="${photoUrl}" alt="${pref.nome}" onerror="this.onerror=null; this.src='${window.getCandidateAvatarUrl(pref.nome, pref.partido)}'">
        <div class="party-badge-floating">${pref.partido}</div>
      </div>
      
      <div class="mayor-info">
        <span class="candidate-number">NÚMERO ${pref.numero}</span>
        <h2>${pref.nome}</h2>
        <p class="party-tagline">Partido: <strong>${pref.partido}</strong> | Situação: <strong style="color:var(--success)">${pref.situacao}</strong></p>
        
        <div class="mayor-voting-results">
          <div class="voting-stats-header">
            <span class="vote-percent">${pref.percentual.toFixed(2)}%</span>
            <span class="vote-count">${votosFormatted} votos válidos</span>
          </div>
          <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: ${pref.percentual}%"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vice-Prefeito -->
    <div class="mayor-vice-row">
      <div class="vice-photo">
        <img src="${photoViceUrl}" alt="${pref.vice}" onerror="this.onerror=null; this.src='${window.getCandidateAvatarUrl(pref.vice, pref.partidoVice)}'">
      </div>
      <div class="vice-info">
        <p>Vice-Prefeito(a)</p>
        <h4>${pref.vice} (${pref.partidoVice})</h4>
      </div>
    </div>

    <!-- Coligação -->
    <div class="mayor-coalition">
      <strong>Coligação de Campanha:</strong><br>
      ${pref.coligacao}
    </div>
  `;

  // Permite clicar na chapa do prefeito para ver detalhes da chapa
  ticketCard.style.cursor = "pointer";
  ticketCard.onclick = () => {
    openDetailsModal({
      nome: pref.nome,
      partido: pref.partido,
      numero: pref.numero,
      votos: pref.votos,
      percentual: pref.percentual,
      situacao: pref.situacao,
      cargo: "PREFEITO (CHAPA COMPLETA)",
      coligacao: pref.coligacao,
      genero: pref.genero || "M",
      vice: pref.vice,
      partidoVice: pref.partidoVice,
      sqcand: pref.sqcand,
      sqcandVice: pref.sqcandVice
    });
  };

  // Atualiza painel estatístico lateral
  const chartFill = document.getElementById("mayor-chart-fill");
  const chartText = document.getElementById("mayor-chart-text");
  const legendWinnerName = document.getElementById("legend-winner-name");
  const legendWinnerVotes = document.getElementById("legend-winner-votes");
  const legendOthersVotes = document.getElementById("legend-others-votes");
  
  const validVotesVal = document.getElementById("stat-valid-votes");
  const abstentionVotesVal = document.getElementById("stat-abstention-votes");

  // Ajusta stroke do chart circular
  const dashArray = `${pref.percentual.toFixed(0)}, 100`;
  chartFill.setAttribute("stroke-dasharray", dashArray);
  chartText.innerText = `${pref.percentual.toFixed(1)}%`;

  legendWinnerName.innerText = pref.nome;
  legendWinnerVotes.innerText = `${votosFormatted} votos`;

  const outrosVotosVal = data.votosValidos - pref.votos;
  legendOthersVotes.innerText = `${outrosVotosVal.toLocaleString("pt-BR")} votos`;

  validVotesVal.innerText = data.votosValidos.toLocaleString("pt-BR");
  
  // Abstenção real ou fictícia coerente por semente
  let abstPercent = data.abstencao;
  if (!abstPercent) {
    const rand = createSeededRandom(pref.nome);
    abstPercent = 18 + (rand() * 7);
  }
  abstentionVotesVal.innerText = `${abstPercent.toFixed(2)}%`;
}

// Renderizador genérico para as grids de candidatos (Vereador, Senador, Deputado)
function renderCandidatesGrid(gridId, candidates, cargoLabel) {
  const grid = document.getElementById(gridId);
  grid.innerHTML = "";
  const uf = appState.selectedState;

  candidates.forEach((cand, index) => {
    const card = document.createElement("div");
    
    // Resolve texto de situação (principalmente para 2022 onde não há campo situacao no JSON)
    let situacaoText = cand.situacao;
    if (!situacaoText) {
      situacaoText = `${index + 1}º Mais Votado`;
    }
    
    // Classes de status
    let sitClass = "outros";
    let borderClass = "";
    if (situacaoText.startsWith("Eleito") || situacaoText.includes("1º")) {
      sitClass = "eleito";
      borderClass = "eleito";
    } else if (situacaoText.includes("Suplente") || situacaoText.includes("2º") || situacaoText.includes("3º")) {
      sitClass = "suplente";
      borderClass = "suplente";
    }

    card.className = `candidate-card card-glass ${borderClass}`;
    card.setAttribute("data-name", cand.nomeUrna || cand.nome);
    card.setAttribute("data-party", cand.partido);
    
    // Resolve nomenclatura do cargo se for DF
    const resolvedCargoLabel = cargoLabel === "DEP. ESTADUAL" && uf === "DF" ? "DEP. DISTRITAL" : cargoLabel;
    
    // Resolve o ano de eleição para carregar a foto correta
    const year = resolvedCargoLabel === "VEREADOR" ? 2024 : 2022;
    const photoUrl = window.getCandidatePhotoUrl(uf, cand.sqcand, year) || window.getCandidateAvatarUrl(cand.nomeUrna || cand.nome, cand.partido);
    const votosFormatted = cand.votos.toLocaleString("pt-BR");

    card.innerHTML = `
      <div class="cand-photo-wrapper">
        <img src="${photoUrl}" alt="${cand.nomeUrna || cand.nome}" onerror="this.onerror=null; this.src='${window.getCandidateAvatarUrl(cand.nomeUrna || cand.nome, cand.partido)}'">
      </div>
      <div class="cand-meta">
        <div class="cand-header-row">
          <span class="cand-number">#${cand.numero}</span>
          <span class="cand-status-tag status-${sitClass}">${situacaoText}</span>
        </div>
        <h4 class="cand-name" title="${cand.nomeUrna || cand.nome}">${cand.nomeUrna || cand.nome}</h4>
        <div class="cand-party-box">
          <span class="cand-party-badge">${cand.partido}</span>
        </div>
        <div class="cand-votes-row">
          <span class="cand-votes-count">${votosFormatted} votos</span>
          <span class="cand-votes-percent">${cand.percentual.toFixed(2)}%</span>
        </div>
      </div>
    `;

    // Abertura de modal de detalhes ao clicar
    card.addEventListener("click", () => {
      openDetailsModal({
        nome: cand.nome,
        nomeUrna: cand.nomeUrna,
        partido: cand.partido,
        numero: cand.numero,
        votos: cand.votos,
        percentual: cand.percentual,
        situacao: situacaoText,
        cargo: resolvedCargoLabel,
        genero: cand.genero,
        sqcand: cand.sqcand
      });
    });

    grid.appendChild(card);
  });
}

// --- MODAL DE DETALHES ---

function setupModal() {
  modalCloseBtn.addEventListener("click", closeModal);
  modalBtnConfirm.addEventListener("click", closeModal);
  
  // Fecha clicando no fundo escuro
  candidateModal.addEventListener("click", (e) => {
    if (e.target === candidateModal) {
      closeModal();
    }
  });

  // Fechamento no ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && candidateModal.classList.contains("show")) {
      closeModal();
    }
  });
}

function openDetailsModal(cand) {
  // Define Avatar usando foto oficial do TSE se houver sqcand
  modalAvatarPlaceholder.innerHTML = "";
  const img = document.createElement("img");
  const isChapa = cand.cargo.includes("PREFEITO");
  const year = isChapa || cand.cargo.includes("VEREADOR") ? 2024 : 2022;
  const photoUrl = window.getCandidatePhotoUrl(appState.selectedState, cand.sqcand, year) || window.getCandidateAvatarUrl(cand.nomeUrna || cand.nome, cand.partido);
  
  img.src = photoUrl;
  img.alt = cand.nome;
  img.onerror = () => {
    img.onerror = null;
    img.src = window.getCandidateAvatarUrl(cand.nomeUrna || cand.nome, cand.partido);
  };
  modalAvatarPlaceholder.appendChild(img);

  // Define Metadados
  modalBadgeCargo.innerText = cand.cargo;
  modalCandidateName.innerText = cand.nome;
  modalCandidateParty.innerText = cand.partido;
  modalCandidatePartyNumber.innerText = cand.numero.toString().substring(0, 2);
  
  // Busca o nome do partido completo
  const partyInfo = window.PARTIDOS.find(p => p.sigla === cand.partido);
  modalCandidatePartyName.innerText = partyInfo ? partyInfo.nome : "Partido Político";

  // Define Estatísticas
  modalStatVotes.innerText = cand.votos.toLocaleString("pt-BR");
  modalStatPercent.innerText = `${cand.percentual.toFixed(2)}%`;
  modalStatSituation.innerText = cand.situacao;

  // Ajusta cor da situação do modal
  modalStatSituation.className = "modal-stat-value";
  if (cand.situacao.startsWith("Eleito") || cand.situacao.includes("1º")) {
    modalStatSituation.classList.add("status-color-positive");
  } else if (cand.situacao.includes("Suplente") || cand.situacao.includes("2º") || cand.situacao.includes("3º")) {
    modalStatSituation.classList.add("status-color-warning");
  } else {
    modalStatSituation.classList.add("status-color-neutral");
  }

  // Define Detalhes de Texto
  modalDetailNumber.innerText = cand.numero;
  modalDetailJurisdiction.innerText = `${appState.selectedCity} (${appState.selectedState})`;
  
  modalDetailYear.innerText = isChapa || cand.cargo.includes("VEREADOR") ? "2024 (Municipais)" : "2022 (Gerais)";

  if (isChapa) {
    modalRowColigacao.style.display = "flex";
    modalDetailColigacao.innerText = cand.coligacao || "Não informada";
  } else {
    modalRowColigacao.style.display = "none";
  }

  // Se for prefeito (chapa), exibe também os detalhes do vice
  let modalRowVice = document.getElementById("modal-row-vice");
  if (isChapa && cand.vice) {
    if (!modalRowVice) {
      modalRowVice = document.createElement("div");
      modalRowVice.className = "detail-row";
      modalRowVice.id = "modal-row-vice";
      modalRowVice.innerHTML = `
        <span class="detail-label">Vice-Prefeito:</span>
        <span class="detail-value" id="modal-detail-vice"></span>
      `;
      modalRowColigacao.parentNode.insertBefore(modalRowVice, modalRowColigacao);
    }
    modalRowVice.style.display = "flex";
    document.getElementById("modal-detail-vice").innerText = `${cand.vice} (${cand.partidoVice})`;
  } else if (modalRowVice) {
    modalRowVice.style.display = "none";
  }

  // Ajusta barra de progresso visual (percentual relativo de votos válidos)
  modalProgressBar.style.width = `${Math.min(cand.percentual * 2, 100)}%`; // Escala multiplicada por 2 para melhor visibilidade

  // Mostra o Modal
  candidateModal.classList.add("show");
}

function closeModal() {
  candidateModal.classList.remove("show");
}

// Cria gerador semente para abstenção no escopo local
function createSeededRandom(seedString) {
  let h = 0;
  for (let i = 0; i < seedString.length; i++) {
    h = Math.imul(31, h) + seedString.charCodeAt(i) | 0;
  }
  return function() {
    let t = h += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
