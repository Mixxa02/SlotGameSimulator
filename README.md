# Slot Game Simulator 🎰

Ovaj projekat simulira video slot igru sa 5 rilova i 3 reda, uključujući:  

- Industry-standard payline evaluaciju  
- Wild simbole koji zamenjuju najbolje dobitke  
- Scatter simbole koji pokreću free spinove sa retriggerima  
- Izračunavanje ključnih metrika: RTP, Hit Frequency, Volatilnost i Max Win  
- Histogram raspodele dobitaka  

## Funkcionalnosti

- **Modularna logika igre**: spinovi, linije, simboli, free spinovi  
- **Statistika**: RTP, učestalost dobitaka, standardna devijacija, maksimalni dobitak  
- **Vizualizacija**: Histogram dobitaka (log skala)  
- **Portfolio-ready**: jedan fajl, lako deljenje i pokretanje  

## Instalacija

1. Kloniraj repo:
```bash
git clone https://github.com/Mixxa02/SlotGameSimulator.git
cd SlotGameSimulator
```
2. Instaliraj zavisnosti:
```bash
pip install matplotlib
```

3. Pokretanje simulacije
```bash
python slot_simulator.py
```
Skripta će ispisati RTP, hit frequency, volatilnost i maksimalni dobitak.
Otvoriće histogram raspodele dobitaka (logaritamska skala).
Spins: default 100,000 (možeš povećati za precizniju statistiku)
Total Bet: default 1.0 (deljeno po 10 paylines)
