"""HTML templates for the web interface."""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech News Aggregator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            padding: 20px;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .controls label {
            font-weight: 600;
            color: #555;
        }
        
        .controls input {
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            width: 100px;
        }
        
        .controls button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }
        
        .controls button:hover {
            background: #5568d3;
        }
        
        .controls button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .status {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: none;
        }
        
        .status.error {
            background: #fee;
            border-left: 4px solid #f44;
            color: #c33;
        }
        
        .status.success {
            background: #efe;
            border-left: 4px solid #4f4;
            color: #3c3;
        }
        
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .news-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
        }
        
        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }
        
        .news-card-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }
        
        .news-source {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .news-source.hackernews {
            background: #ff6600;
            color: white;
        }
        
        .news-source.rss {
            background: #4a90e2;
            color: white;
        }
        
        .news-score {
            background: #f0f0f0;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 600;
            color: #666;
        }
        
        .news-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 10px;
            line-height: 1.4;
            color: #333;
        }
        
        .news-title a {
            color: #667eea;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .news-title a:hover {
            color: #5568d3;
            text-decoration: underline;
        }
        
        .news-meta {
            display: flex;
            gap: 15px;
            margin-top: auto;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }
        
        .news-date {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .news-comments {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .news-comments a {
            color: #667eea;
            text-decoration: none;
        }
        
        .news-comments a:hover {
            text-decoration: underline;
        }
        
        .news-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 10px;
        }
        
        .news-tag {
            background: #f0f0f0;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            color: #666;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: white;
            font-size: 1.2em;
        }
        
        .spinner {
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: white;
            font-size: 1.1em;
        }
        
        @media (max-width: 768px) {
            .news-grid {
                grid-template-columns: 1fr;
            }
            
            header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 Tech News Aggregator</h1>
            <p>Dernières actualités tech depuis Hacker News et RSS</p>
        </header>
        
        <div class="controls">
            <label for="limit">Nombre d'articles:</label>
            <input type="number" id="limit" min="1" max="50" value="20">
            <button onclick="loadNews()">Charger les news</button>
            <button onclick="loadNews(true)" id="refreshBtn">🔄 Actualiser</button>
        </div>
        
        <div id="status" class="status"></div>
        
        <div id="loading" class="loading" style="display: none;">
            <div class="spinner"></div>
            <p>Chargement des news...</p>
        </div>
        
        <div id="news-container" class="news-grid"></div>
    </div>
    
    <script>
        async function loadNews(showLoading = true) {
            const limit = document.getElementById('limit').value || 20;
            const container = document.getElementById('news-container');
            const loading = document.getElementById('loading');
            const status = document.getElementById('status');
            const refreshBtn = document.getElementById('refreshBtn');
            
            // Reset
            status.style.display = 'none';
            status.className = 'status';
            container.innerHTML = '';
            
            if (showLoading) {
                loading.style.display = 'block';
            }
            refreshBtn.disabled = true;
            
            try {
                const response = await fetch(`/news?limit=${limit}`);
                const data = await response.json();
                
                loading.style.display = 'none';
                refreshBtn.disabled = false;
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Erreur lors du chargement');
                }
                
                // Show status if sources failed
                if (data.meta && data.meta.failed_sources && data.meta.failed_sources.length > 0) {
                    status.textContent = `⚠️ Certaines sources ont échoué: ${data.meta.failed_sources.join(', ')}`;
                    status.className = 'status error';
                    status.style.display = 'block';
                }
                
                if (data.items && data.items.length > 0) {
                    renderNews(data.items);
                } else {
                    container.innerHTML = '<div class="empty-state">Aucune news disponible pour le moment.</div>';
                }
            } catch (error) {
                loading.style.display = 'none';
                refreshBtn.disabled = false;
                status.textContent = `❌ Erreur: ${error.message}`;
                status.className = 'status error';
                status.style.display = 'block';
                container.innerHTML = '<div class="empty-state">Impossible de charger les news.</div>';
            }
        }
        
        function renderNews(items) {
            const container = document.getElementById('news-container');
            container.innerHTML = '';
            
            items.forEach(item => {
                const card = document.createElement('div');
                card.className = 'news-card';
                
                const date = new Date(item.published_at);
                const dateStr = date.toLocaleDateString('fr-FR', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
                
                card.innerHTML = `
                    <div class="news-card-header">
                        <span class="news-source ${item.source}">${item.source === 'hackernews' ? 'HN' : 'RSS'}</span>
                        ${item.score !== null ? `<span class="news-score">⭐ ${item.score}</span>` : ''}
                    </div>
                    <h2 class="news-title">
                        <a href="${item.url}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.title)}</a>
                    </h2>
                    ${item.tags && item.tags.length > 0 ? `
                        <div class="news-tags">
                            ${item.tags.map(tag => `<span class="news-tag">${escapeHtml(tag)}</span>`).join('')}
                        </div>
                    ` : ''}
                    <div class="news-meta">
                        <span class="news-date">📅 ${dateStr}</span>
                        ${item.comments_url ? `
                            <span class="news-comments">
                                <a href="${item.comments_url}" target="_blank" rel="noopener noreferrer">💬 Commentaires</a>
                            </span>
                        ` : ''}
                    </div>
                `;
                
                container.appendChild(card);
            });
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Load news on page load
        window.addEventListener('DOMContentLoaded', () => {
            loadNews();
        });
        
        // Auto-refresh every 60 seconds
        setInterval(() => {
            loadNews(false);
        }, 60000);
    </script>
</body>
</html>"""
