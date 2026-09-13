# Écrans de chargement — 12 septembre 2026

Ludovic demande de remplacer le fond bleu et le grand texte centré par un fond
noir, un texte en bas à droite et une petite animation graphique. La capture
[avant modification](before.png) est celle qu'il a fournie. L'optimisation des
modèles 3D est reportée ; ce changement concerne uniquement le chargement.

Le composant commun `TheEnd.Client/Composition/LoadingScreen.cs` affiche
désormais un fond noir uni, un libellé gris clair aligné à droite et un anneau de
douze segments dont la lumière tourne en 1,2 seconde. Le texte reste immobile.
Cette présentation s'applique au vaisseau, au plan/pont et aux portraits, dans
les deux modes de rendu. Les libellés et les étapes existants sont conservés.

La taille du texte suit le réglage d'interface (14 pixels de hauteur visible à
100 %), les marges s'adaptent à la fenêtre et les messages longs passent à la
ligne. L'option de mouvement réduit fige l'anneau. Une erreur affiche une croix
fixe et son message en rouge ; un texte plus long que la fenêtre est terminé
par une ellipse. La texture d'un pixel utilisée pour l'indicateur est créée au
chargement et libérée avec le composant. Le fond du monde et les mécanismes de
chargement restent inchangés.

## Aperçus natifs

- [Vaisseau, 1920 × 1080](fr-ship.png).
- [Plan/pont](fr-plan.png) et [portraits](fr-portraits.png).
- [Animation, trois cycles](loading-screen.mp4), 1920 × 1080, 30 images/s.
- [Anglais, 1280 × 720](en-ship.png).
- [Petite fenêtre, interface à 200 %](compact-portraits.png).
- [Erreur longue en petite fenêtre](compact-error-long.png).

Les captures appellent la vraie classe `LoadingScreen` du Client compilé dans
un hôte MonoGame avec la véritable police `Fonts/UI`, puis lisent le backbuffer.
Elles montrent le composant natif aux instants choisis ; la vidéo ne mesure pas
la durée de génération d'une partie. Le petit hôte local se trouve dans
`TheEnd/.artifacts/loading-screen-preview`, avec son `run.ps1`.

Vérification : compilation Client Debug sans avertissement ni erreur, 49 images
natives contrôlées en français/anglais, trois tailles et deux échelles UI. Les
36 images du cycle animé sont distinctes ; les deux captures de mouvement réduit
sont identiques. Les trois fichiers `*-proof.json` conservent les dimensions,
bounds du contenu et empreintes des captures (les images individuelles du cycle
restent dans le cache local). Aucun nouveau test unitaire pour cette retouche
visuelle ; compilation et contrôle natif constituent la vérification effectuée.

Le style demandé est implémenté ; le retour artistique de Ludovic sur ce nouvel
aperçu reste à recueillir. Aucun commit/push Code, Art ou Docs par l'assistant.
