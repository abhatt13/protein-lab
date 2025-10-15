# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Get Token

**POST** `/api/auth/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## Endpoints

### Authentication

#### Register User
**POST** `/api/auth/register`

```json
{
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "securepassword",
  "role": "viewer"
}
```

### Proteins

#### Create Protein
**POST** `/api/proteins/`

Requires: `researcher` role or higher

```json
{
  "uniprot_id": "P12345",
  "name": "Example Protein",
  "sequence": "MKTLLLTLVVVTIVFPSSL...",
  "organism": "Homo sapiens",
  "gene_name": "GENE1",
  "protein_family": "Kinase",
  "function": "Catalyzes the transfer of...",
  "molecular_weight": 45000.0,
  "pdb_id": "1ABC",
  "subcellular_location": "Cytoplasm",
  "keywords": ["kinase", "signaling"],
  "ec_number": "2.7.11.1"
}
```

#### List Proteins
**GET** `/api/proteins/`

Query Parameters:
- `skip`: Pagination offset (default: 0)
- `limit`: Results per page (default: 100)
- `query`: Text search
- `organism`: Filter by organism
- `protein_family`: Filter by family
- `is_validated`: Filter validated proteins

#### Get Protein
**GET** `/api/proteins/{protein_id}`

#### Update Protein
**PUT** `/api/proteins/{protein_id}`

Requires: `researcher` role or higher

```json
{
  "name": "Updated Name",
  "function": "Updated function description"
}
```

#### Delete Protein
**DELETE** `/api/proteins/{protein_id}`

Requires: `admin` role

#### Get Protein Versions
**GET** `/api/proteins/{protein_id}/versions`

Returns version history for a protein.

## Rate Limiting

API requests are rate-limited to 100 requests per minute per IP address.

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Protein not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.
