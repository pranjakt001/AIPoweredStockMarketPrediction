# Deployment Guide

## Production Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites
- Docker installed
- Docker Compose installed

#### Steps

```bash
# Clone repository
git clone <repository-url>
cd AIPoweredStockMarketPrediction

# Configure environment
cp .env.example .env
# Edit .env with production settings

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Access
- Frontend: http://your-domain.com
- API: http://your-domain.com/api

### 2. Traditional Linux Server

#### Prerequisites
- Ubuntu 20.04+ or similar
- Python 3.11+
- Nginx
- Systemd

#### Installation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip nginx -y

# Clone repository
cd /opt
sudo git clone <repository-url>
cd AIPoweredStockMarketPrediction

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit settings
```

#### Systemd Service

Create `/etc/systemd/system/stock-prediction.service`:

```ini
[Unit]
Description=Stock Market Prediction API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/AIPoweredStockMarketPrediction
Environment="PATH=/opt/AIPoweredStockMarketPrediction/venv/bin"
ExecStart=/opt/AIPoweredStockMarketPrediction/venv/bin/gunicorn \
    --bind 127.0.0.1:5000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /var/log/stock-prediction/access.log \
    --error-logfile /var/log/stock-prediction/error.log \
    'backend.app:create_app()'

Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/stock-prediction
sudo chown www-data:www-data /var/log/stock-prediction

# Enable and start service
sudo systemctl enable stock-prediction
sudo systemctl start stock-prediction
sudo systemctl status stock-prediction
```

#### Nginx Configuration

Create `/etc/nginx/sites-available/stock-prediction`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /opt/AIPoweredStockMarketPrediction/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/stock-prediction /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. AWS Deployment

#### EC2 Instance

1. Launch EC2 instance (t3.medium or larger)
2. Install Docker or follow traditional Linux deployment
3. Configure security group (ports 80, 443, 5000)
4. Setup Elastic IP
5. Configure Route 53 for domain

#### ECS (Elastic Container Service)

```bash
# Build image
docker build -t stock-prediction .

# Tag for ECR
docker tag stock-prediction:latest <account-id>.dkr.ecr.region.amazonaws.com/stock-prediction:latest

# Push to ECR
aws ecr get-login-password --region region | docker login --username AWS --password-stdin <account-id>.dkr.ecr.region.amazonaws.com
docker push <account-id>.dkr.ecr.region.amazonaws.com/stock-prediction:latest

# Create ECS task definition and service
```

### 4. Heroku Deployment

Create `Procfile`:

```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 'backend.app:create_app()'
```

Deploy:

```bash
# Login
heroku login

# Create app
heroku create stock-prediction-app

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set API_PORT=$PORT

# Deploy
git push heroku main

# Open app
heroku open
```

### 5. Google Cloud Platform

#### App Engine

Create `app.yaml`:

```yaml
runtime: python311

instance_class: F2

env_variables:
  FLASK_ENV: "production"

automatic_scaling:
  min_instances: 1
  max_instances: 5
```

Deploy:

```bash
gcloud app deploy
```

#### Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/stock-prediction

# Deploy
gcloud run deploy stock-prediction \
  --image gcr.io/PROJECT_ID/stock-prediction \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Environment Variables

Production `.env` file:

```env
FLASK_ENV=production
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False

CORS_ORIGINS=https://your-domain.com

LOG_LEVEL=WARNING

DEFAULT_TICKER=^AXJO
START_DATE=2018-01-01
```

## Monitoring

### Logs

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u stock-prediction -f

# Log files
tail -f /var/log/stock-prediction/error.log
```

### Health Checks

```bash
# API health
curl http://localhost:5000/api/health

# Docker health
docker ps
```

## Backup

```bash
# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup models
tar -czf models-$(date +%Y%m%d).tar.gz data/models/
```

## Scaling

### Horizontal Scaling

1. Deploy multiple instances behind load balancer
2. Use shared storage for data/models
3. Implement Redis for caching
4. Use external database for persistence

### Vertical Scaling

Increase resources:
- RAM: 4GB minimum, 8GB recommended
- CPU: 2 cores minimum, 4 cores recommended
- Disk: 20GB minimum

## Performance Optimization

1. **Enable Caching**
   - Redis for API responses
   - Model prediction caching

2. **Optimize Workers**
   - Gunicorn workers = (2 × CPU cores) + 1

3. **Database**
   - PostgreSQL for production data
   - Connection pooling

4. **CDN**
   - CloudFlare for static assets
   - Faster global delivery

## Security Checklist

- [ ] Change default settings
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Regular security updates
- [ ] Firewall configuration
- [ ] Environment variable security
- [ ] Input validation
- [ ] SQL injection prevention

## Maintenance

### Daily
- Check logs for errors
- Monitor system resources

### Weekly
- Update stock data
- Retrain models
- Check disk space

### Monthly
- Security updates
- Dependency updates
- Backup verification

## Troubleshooting

### API Not Starting

```bash
# Check logs
docker-compose logs api

# Check port
sudo netstat -tulpn | grep 5000

# Restart service
sudo systemctl restart stock-prediction
```

### High Memory Usage

```bash
# Check memory
free -h

# Reduce workers
# Edit gunicorn workers count
```

### Slow Predictions

- Increase timeout in gunicorn
- Add more workers
- Optimize model code
- Use caching

## Support

For issues:
1. Check logs
2. Review documentation
3. Open GitHub issue
4. Contact support
