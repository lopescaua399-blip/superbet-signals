"""
Script de exemplo de uso
"""
from src.analyzer import BettingAnalyzer


def main():
    """Exemplo de uso do analisador"""

    # Inicializar
    analyzer = BettingAnalyzer()

    print("=" * 60)
    print("🎯 SUPERBET SIGNALS - Robô de Análise de Apostas")
    print("=" * 60)

    # Jogos para análise
    games = [
        {
            "home_team": "Flamengo",
            "away_team": "Vasco",
            "date": "2026-05-14",
            "odds": {
                "over_2_5": 1.85,
                "under_2_5": 1.95,
                "home_win": 1.65,
                "away_win": 4.20,
                "draw": 3.40
            }
        },
        {
            "home_team": "Santos",
            "away_team": "Palmeiras",
            "date": "2026-05-14",
            "odds": {
                "over_2_5": 1.95,
                "under_2_5": 1.85,
                "home_win": 2.80,
                "away_win": 2.50,
                "draw": 3.20
            }
        }
    ]

    # Analisar todos os jogos
    print("\n📊 Analisando jogos...")
    results = analyzer.analyze_multiple_games(games)

    # Exibir resultados
    for result in results:
        print(f"\n{'=' * 60}")
        print(f"🏟️  {result['match']}")
        print(f"📅 {result['date']}")
        print(f"{'=' * 60}")

        if result["signals"]:
            print(f"\n✅ Sinais Identificados:")
            for i, signal in enumerate(result["signals"], 1):
                print(f"\n  {i}. {signal['name']}")
                print(f"     Probabilidade: {signal['probability']:.1%}")
                print(f"     Confiança: {signal['confidence']:.1%}")
                print(f"     Recomendação: {signal['recommendation']}")
                if "odds" in signal:
                    print(f"     Odds: {signal['odds']:.2f}")
                    print(f"     Valor Esperado: {signal['expected_value']:+.1f}%")
        else:
            print("\n❌ Sem sinais qualificados")

    # Filtrar melhores sinais
    print(f"\n{'=' * 60}")
    print("🏆 MELHORES SINAIS")
    print(f"{'=' * 60}\n")

    best_signals = analyzer.get_best_signals(
        results,
        min_probability=0.70,
        min_confidence=0.75
    )

    if best_signals:
        for i, signal in enumerate(best_signals, 1):
            print(
                f"{i}. {signal['match']} - {signal['name']}\n"
                f"   📊 {signal['probability']:.1%} | "
                f"💪 {signal['confidence']:.1%} | "
                f"{signal['recommendation']}\n"
            )
    else:
        print("Nenhum sinal de alta confiança encontrado.\n")

    print(f"{'=' * 60}")
    print("📋 Disclaimer: Análise para fins educacionais.")
    print("   Apostas envolvem risco. Use com responsabilidade.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
