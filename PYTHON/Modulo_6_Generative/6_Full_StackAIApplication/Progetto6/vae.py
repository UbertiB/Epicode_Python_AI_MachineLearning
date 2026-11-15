"""
FASE 2 - GENERATIVE CORE: VAE PER DATI TABELLARI

- Encoder: vettore di input -> media (mu) e log-varianza (logvar) dello spazio latente
- Reparameterization trick: z = mu + epsilon * std, così il gradiente può passare
- Decoder: punto z dello spazio latente -> vettore ricostruito
- Loss: Reconstruction Loss (MSE) + beta * KL Divergence

Con dati tabellari usiamo solo strati densi (Fully Connected), non convoluzioni.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Selezione del dispositivo di calcolo: GPU se disponibile, altrimenti CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# -----------------------------------------------------------------------------
# 1. ARCHITETTURA DEL MODELLO
# -----------------------------------------------------------------------------
class TabularVAE(nn.Module):
    def __init__(self, n_input: int, latent_dim: int = 8, hidden: int = 64):
        super().__init__()
        self.latent_dim = latent_dim

        # L'encoder comprime il vettore di input in una rappresentazione intermedia
        self.encoder = nn.Sequential(
            nn.Linear(n_input, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden // 2),
            nn.ReLU(),
        )
        # Due "teste" separate: una per la media, una per la log-varianza
        self.fc_mu = nn.Linear(hidden // 2, latent_dim)
        self.fc_logvar = nn.Linear(hidden // 2, latent_dim)

        # Il decoder fa il percorso inverso. La Sigmoid finale produce valori tra 0 e 1,
        # coerenti con MinMaxScaler e One-Hot Encoding.
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden // 2),
            nn.ReLU(),
            nn.Linear(hidden // 2, hidden),
            nn.ReLU(),
            nn.Linear(hidden, n_input),
            nn.Sigmoid(),
        )

    def encode(self, x):
        """Restituisce media e log-varianza della distribuzione latente."""
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        """
        Reparameterization trick: invece di campionare z direttamente (operazione non derivabile),
        campioniamo epsilon da una Normale(0,1) e calcoliamo z = mu + epsilon * std.
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        """Input -> Encoder -> Reparametrizzazione -> Decoder -> Output."""
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decoder(z), mu, logvar


# -----------------------------------------------------------------------------
# 2. LOSS FUNCTION
# -----------------------------------------------------------------------------
def loss_vae(recon, x, mu, logvar, beta: float = 0.05):
    """
    Reconstruction Loss (MSE): quanto il vettore ricostruito è fedele all'originale.
    KL Divergence: quanto la distribuzione latente si allontana da una Normale standard.
    Entrambe sono divise per la dimensione del batch, per avere valori medi per record.

    Perché beta < 1: con dati scalati tra 0 e 1 la MSE è piccola, e con beta = 1 la KL prevale.
    Il modello allora ignora l'input e restituisce sempre la media (posterior collapse):
    dati sintetici tutti uguali. Con beta = 0.05 le due componenti sono bilanciate.
    """
    recon_loss = F.mse_loss(recon, x, reduction="sum") / x.size(0)
    kld = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / x.size(0)
    return recon_loss + beta * kld, recon_loss, kld


# -----------------------------------------------------------------------------
# 3. ADDESTRAMENTO
# -----------------------------------------------------------------------------
def addestra(X: np.ndarray, latent_dim=8, epochs=300, batch_size=64, lr=1e-3,
             beta=0.05, seed=42, callback=None):
    """
    Addestra il VAE sulla matrice preprocessata.

    callback: funzione facoltativa chiamata alla fine di ogni epoca con le loss dell'epoca.
    Serve al backend per mostrare l'avanzamento mentre il training gira in background.

    Returns:
        (modello addestrato, storico delle loss per epoca)
    """
    torch.manual_seed(seed)
    dati = torch.tensor(X, dtype=torch.float32)
    loader = torch.utils.data.DataLoader(dati, batch_size=batch_size, shuffle=True)

    model = TabularVAE(n_input=X.shape[1], latent_dim=latent_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    storico = []

    model.train()
    for epoch in range(epochs):
        totale = ricostruzione = kl = 0.0
        for batch in loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            recon, mu, logvar = model(batch)
            loss, recon_loss, kld = loss_vae(recon, batch, mu, logvar, beta)
            loss.backward()
            optimizer.step()
            # Pesiamo per il numero di righe del batch (l'ultimo può essere più piccolo)
            n = batch.size(0)
            totale += loss.item() * n
            ricostruzione += recon_loss.item() * n
            kl += kld.item() * n

        storico.append({
            "epoca": epoch + 1,
            "loss": totale / len(dati),
            "ricostruzione": ricostruzione / len(dati),
            "kl": kl / len(dati),
        })
        if callback:
            callback(storico[-1])

    # Errore di ricostruzione residuo per ogni colonna: serve in fase di generazione (vedi genera)
    model.eval()
    with torch.no_grad():
        recon, _, _ = model(dati.to(device))
        model.sigma_rumore = (recon - dati.to(device)).std(dim=0)
    return model, storico


# -----------------------------------------------------------------------------
# 4. GENERAZIONE (SAMPLING)
# -----------------------------------------------------------------------------
@torch.no_grad()
def genera(model: TabularVAE, n_righe: int, seed: int | None = None) -> np.ndarray:
    """
    L'encoder viene "spento": campioniamo vettori casuali da una Normale(0,1)
    nello spazio latente e li passiamo solo al decoder.

    Il decoder restituisce il valore MEDIO atteso per quel punto z (la MSE equivale a
    ipotizzare un errore gaussiano intorno a questa media). Usare solo la media produce dati
    troppo "lisci", con varianza molto più bassa del reale. Per questo aggiungiamo
    il rumore gaussiano stimato a fine training: è il campionamento completo da p(x|z).
    """
    if seed is not None:
        torch.manual_seed(seed)
    model.eval() #encoder spento
    z = torch.randn(n_righe, model.latent_dim, device=device)
    media = model.decoder(z)
    rumore = torch.randn_like(media) * model.sigma_rumore
    return (media + rumore).cpu().numpy()
