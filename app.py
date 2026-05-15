#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Superbet Signals - Robô de Análise de Apostas
Versão: 1.0
"""

from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)


class BettingSignal:
    """Classe para representar um sinal de aposta"""
    
    def __init__(self, match, signal_type, probability, confidence, recommendation):
        self.match = match
        self.signal_type = signal_type
        self.probability = probability
        self.confidence = confidence
        self.recommendation = recommendation
    
    def to_dict(self):
        return {
            'match': self.match,
            'type': self.signal_type,
            'probability': f"{self.probability:.1%}",
            'confidence': f"{self.confidence:.1%}",
            'recommendation': self.recommendation
        }


class BettingAnalyzer:
    """Analisador de jogos de apostas"""
    
    def __init__(self):
        self.signals = []
        self.analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def analyze_game(self, home_team, away_team, odds):
        """Analisa um jogo e gera sinais"""
        match_name = f"{home_team} vs {away_team}"
        signals = []
        
        # Análise Over/Under
        if odds.get('over_2_5', 0) > 0:
            probability = 0.65 + (odds.get('over_2_5', 1.95) - 1.85) * 0.5
            probability = min(0.95, max(0.45, probability))
            confidence = 0.78
            
            if probability > 0.70:
                signal = BettingSignal(
                    match_name,
                    'Over 2.5',
                    probability,
                    confidence,
                    '🔥 FORTE' if probability > 0.80 else '✅ BOM'
                )
                signals.append(signal)
        
        # Análise Vitória Casa
        if odds.get('home_win', 0) > 0:
            probability = 1.0 / odds.get('home_win', 2.0)
            confidence = 0.72 if probability > 0.45 else 0.55
            
            if probability > 0.65:
                signal = BettingSignal(
                    match_name,
                    'Casa Vence',
                    probability,
                    confidence,
                    '🔥 FORTE' if probability > 0.75 else '✅ BOM'
                )
                signals.append(signal)
        
        return signals
    
    def get_all_signals(self):
        """Retorna todos os sinais"""
        games = [
            {
                'home': 'Flamengo',
                'away': 'Vasco',
                'odds': {
                    'over_2_5': 1.85,
                    'under_2_5': 1.95,
                    'home_win': 1.65,
                    'away_win': 4.20,
                    'draw': 3.40
                }
            },
            {
                'home': 'Santos',
                'away': 'Palmeiras',
                'odds': {
                    'over_2_5': 1.95,
                    'under_2_5': 1.85,
                    'home_win': 2.80,
                    'away_win': 2.50,
                    'draw': 3.20
                }
            }
        ]
        
        all_signals = []
        for game in games:
            signals = self.analyze_game(game['home'], game['away'], game['odds'])
            all_signals.extend(signals)
        
        return all_signals


# Instanciar analisador
analyzer = BettingAnalyzer()


@app.route('/')
def index():
    """Página inicial"""
    return jsonify({
        'status': 'online',
        'app': 'Superbet Signals',
        'version': '1.0',
        'message': 'Robô de análise de apostas com sinais de alta probabilidade',
        'endpoints': {
            'signals': '/api/signals',
            'status': '/api/status',
            'health': '/health'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/signals')
def get_signals():
    """Retorna os sinais de apostas"""
    signals = analyzer.get_all_signals()
    return jsonify({
        'status': 'success',
        'total_signals': len(signals),
        'signals': [s.to_dict() for s in signals],
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/status')
def get_status():
    """Retorna o status do robô"""
    return jsonify({
        'status': 'running',
        'app': 'Superbet Signals',
        'uptime': 'active',
        'last_analysis': analyzer.analysis_time,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """Health check para Render"""
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(404)
def not_found(e):
    """Tratador de erro 404"""
    return jsonify({
        'error': 'Not Found',
        'message': 'O endpoint solicitado não existe',
        'available_endpoints': {
            'root': '/',
            'signals': '/api/signals',
            'status': '/api/status',
            'health': '/health'
        }
    }), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
