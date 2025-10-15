# Deployment Guide

## Production Deployment

### Prerequisites

- Docker and Docker Compose
- Domain name (optional)
- SSL certificate (for HTTPS)
- Cloud provider account (AWS, GCP, or Azure)

## Docker Deployment

### 1. Prepare Environment

```bash
cp .env.example .env
```

Edit `.env` with production values:
```bash
DATABASE_URL=postgresql://user:password@db-host:5432/proteinlab
REDIS_URL=redis://redis-host:6379/0
OPENAI_API_KEY=your_production_key
JWT_SECRET_KEY=your_secure_secret_key
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 2. Build Images

```bash
docker-compose -f docker-compose.prod.yml build
```

### 3. Start Services

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Initialize Database

```bash
docker-compose exec api alembic upgrade head
docker-compose exec api python scripts/init_db.py
```

### 5. Set Up Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/proteinlab`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/proteinlab /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 6. SSL with Let's Encrypt

```bash
certbot --nginx -d your-domain.com
```

## AWS Deployment

### Using EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance Type: t3.medium or larger
   - Security Groups: 22, 80, 443, 8000, 8501

2. **Connect and Install Docker**
```bash
ssh ubuntu@your-instance-ip
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu
```

3. **Deploy Application**
```bash
git clone your-repo
cd protein-lab
cp .env.example .env
# Edit .env
docker-compose up -d
```

### Using ECS (Elastic Container Service)

1. **Push images to ECR**
```bash
aws ecr create-repository --repository-name proteinlab-api
aws ecr create-repository --repository-name proteinlab-ui

docker tag proteinlab-api:latest account-id.dkr.ecr.region.amazonaws.com/proteinlab-api:latest
docker push account-id.dkr.ecr.region.amazonaws.com/proteinlab-api:latest
```

2. **Create ECS Task Definition**
3. **Create ECS Service**
4. **Set up Application Load Balancer**

### Using RDS for Database

1. **Create RDS PostgreSQL Instance**
2. **Update DATABASE_URL in .env**
3. **Run migrations**

## GCP Deployment

### Using Cloud Run

1. **Build and push to Container Registry**
```bash
gcloud builds submit --tag gcr.io/project-id/proteinlab-api
gcloud builds submit --tag gcr.io/project-id/proteinlab-ui
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy proteinlab-api \
  --image gcr.io/project-id/proteinlab-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy proteinlab-ui \
  --image gcr.io/project-id/proteinlab-ui \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Kubernetes Deployment

Create deployment files and apply:

```bash
kubectl apply -f k8s/
```

## Monitoring

### Set Up Logging

```bash
docker-compose logs -f
```

### Health Checks

- API: http://your-domain/health
- Streamlit: http://your-domain/_stcore/health

### Backup Database

```bash
docker-compose exec postgres pg_dump -U postgres proteinlab > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker-compose exec -T postgres psql -U postgres proteinlab
```

## Scaling

### Horizontal Scaling

Increase replicas in docker-compose:

```yaml
services:
  api:
    deploy:
      replicas: 3
```

### Vertical Scaling

Update resource limits:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

## Security Checklist

- [ ] Change default passwords
- [ ] Use strong JWT_SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Enable rate limiting
- [ ] Use secrets management
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

## Maintenance

### Update Application

```bash
git pull
docker-compose build
docker-compose up -d
```

### Database Migrations

```bash
docker-compose exec api alembic upgrade head
```

### Clear Cache

```bash
docker-compose exec redis redis-cli FLUSHALL
```
