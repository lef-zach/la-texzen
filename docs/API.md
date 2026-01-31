# API Reference

Complete API documentation for LaTeXZen Scientific Paper Converter.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User

**Endpoint:** `POST /register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "User Name",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `201 Created` - User registered successfully
- `400 Bad Request` - Email already registered or invalid data

---

#### Login

**Endpoint:** `POST /token`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200 OK` - Login successful
- `400 Bad Request` - Invalid credentials

---

#### Get Current User

**Endpoint:** `GET /users/me`

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "User Name",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Status Codes:**
- `200 OK` - User found
- `401 Unauthorized` - Invalid or missing token

---

### Teams

#### Create Team

**Endpoint:** `POST /teams`

**Request Body:**
```json
{
  "name": "Research Team",
  "description": "Our research collaboration team"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Research Team",
  "description": "Our research collaboration team",
  "created_by": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Status Codes:**
- `201 Created` - Team created successfully
- `401 Unauthorized` - Not authenticated

---

#### Get User's Teams

**Endpoint:** `GET /teams`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Research Team",
    "description": "Our research collaboration team",
    "role": "owner",
    "joined_at": "2024-01-01T00:00:00"
  }
]
```

---

#### Get Team Details

**Endpoint:** `GET /teams/{team_id}`

**Response:**
```json
{
  "id": 1,
  "name": "Research Team",
  "description": "Our research collaboration team",
  "created_by": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Status Codes:**
- `200 OK` - Team found
- `403 Forbidden` - Not authorized to access team
- `404 Not Found` - Team not found

---

#### Join Team

**Endpoint:** `POST /teams/{team_id}/join`

**Response:**
```json
{
  "message": "Successfully joined the team"
}
```

**Status Codes:**
- `200 OK` - Joined successfully
- `400 Bad Request` - Already a member or team not found
- `404 Not Found` - Team not found

---

#### Leave Team

**Endpoint:** `POST /teams/{team_id}/leave`

**Response:**
```json
{
  "message": "Successfully left the team"
}
```

**Status Codes:**
- `200 OK` - Left successfully
- `400 Bad Request` - Not a member or owner cannot leave

---

#### Get Team Members

**Endpoint:** `GET /teams/{team_id}/members`

**Response:**
```json
[
  {
    "id": 1,
    "email": "user1@example.com",
    "name": "User 1",
    "role": "owner",
    "joined_at": "2024-01-01T00:00:00"
  },
  {
    "id": 2,
    "email": "user2@example.com",
    "name": "User 2",
    "role": "member",
    "joined_at": "2024-01-02T00:00:00"
  }
]
```

---

#### Remove Team Member

**Endpoint:** `DELETE /teams/{team_id}/members/{user_id}`

**Response:**
```json
{
  "message": "Successfully removed member from team"
}
```

**Status Codes:**
- `200 OK` - Member removed
- `403 Forbidden` - Not authorized to remove members
- `404 Not Found` - User not in team

---

### Templates

#### Create Template

**Endpoint:** `POST /templates`

**Request Body:**
```json
{
  "name": "Custom IEEE Template",
  "content": "\\documentclass{article}\n\\title{Title Here}\n\\begin{document}\n\\maketile\\end{document}",
  "visibility": "private"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Custom IEEE Template",
  "type": "user",
  "visibility": "private",
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00"
}
```

---

#### Get All Templates

**Endpoint:** `GET /templates`

**Response:**
```json
[
  {
    "id": 1,
    "name": "IEEE Conference",
    "type": "global",
    "visibility": "public",
    "owner_id": null,
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": 2,
    "name": "MDPI Journal",
    "type": "global",
    "visibility": "public",
    "owner_id": null,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

#### Get Template Details

**Endpoint:** `GET /templates/{template_id}`

**Response:**
```json
{
  "id": 1,
  "name": "IEEE Conference",
  "type": "global",
  "content": "\\documentclass[conference]{IEEEtran}...",
  "visibility": "public",
  "owner_id": null,
  "team_id": null,
  "category_id": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

#### Update Template Visibility

**Endpoint:** `PATCH /templates/{template_id}/visibility`

**Request Body:**
```json
{
  "visibility": "public"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "IEEE Conference",
  "visibility": "public"
}
```

---

#### Delete Template

**Endpoint:** `DELETE /templates/{template_id}`

**Response:**
```json
{
  "message": "Template deleted successfully"
}
```

---

#### Get Template Categories

**Endpoint:** `GET /template-categories`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Engineering",
    "description": "Engineering and technology journals",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

#### Create Template Category

**Endpoint:** `POST /template-categories`

**Request Body:**
```json
{
  "name": "Medical",
  "description": "Medical and health sciences journals"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Medical",
  "description": "Medical and health sciences journals",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Documents

#### Create Document

**Endpoint:** `POST /documents`

**Request Body:**
```json
{
  "title": "My Research Paper",
  "content": "\\section{Introduction}\nThis is my research paper...",
  "template_id": 1,
  "visibility": "personal"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "My Research Paper",
  "content": "\\section{Introduction}\nThis is my research paper...",
  "template_id": 1,
  "owner_id": 1,
  "visibility": "personal",
  "created_at": "2024-01-01T00:00:00"
}
```

---

#### Get User's Documents

**Endpoint:** `GET /documents`

**Response:**
```json
[
  {
    "id": 1,
    "title": "My Research Paper",
    "template_id": 1,
    "template_name": "IEEE Conference",
    "visibility": "personal",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

---

#### Get Document Details

**Endpoint:** `GET /documents/{document_id}`

**Response:**
```json
{
  "id": 1,
  "title": "My Research Paper",
  "content": "\\section{Introduction}\nThis is my research paper...",
  "template_id": 1,
  "template_name": "IEEE Conference",
  "visibility": "personal",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

#### Update Document

**Endpoint:** `PATCH /documents/{document_id}`

**Request Body:**
```json
{
  "title": "Updated Research Paper",
  "content": "\\section{Updated Introduction}\nThis is my updated research paper...",
  "visibility": "team"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Research Paper",
  "content": "\\section{Updated Introduction}\nThis is my updated research paper...",
  "visibility": "team",
  "updated_at": "2024-01-02T00:00:00"
}
```

---

#### Delete Document

**Endpoint:** `DELETE /documents/{document_id}`

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

---

#### Convert Document

**Endpoint:** `POST /documents/{document_id}/convert?target_format=pdf`

**Response:**
```json
{
  "success": true,
  "message": "Document converted to pdf successfully",
  "data": {
    "content": "<binary PDF data>",
    "format": "pdf",
    "metadata": {
      "format": "PDF",
      "compiled_at": "2024-01-01T00:00:00"
    }
  }
}
```

---

#### Export Document

**Endpoint:** `GET /documents/{document_id}/export?format=tex`

**Response:**
```json
{
  "success": true,
  "content": "\\section{Introduction}\n...",
  "format": "tex"
}
```

---

### Files

#### Upload File

**Endpoint:** `POST /upload`

**Content-Type:** `multipart/form-data`

**Request Body:**
```
file: [binary file]
```

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "abc123.pdf",
  "original_filename": "document.pdf",
  "file_format": "PDF",
  "file_size": 1024000,
  "file_path": "documents/uploads/abc123.pdf",
  "uploaded_at": "2024-01-01T00:00:00"
}
```

**Supported Formats:**
- PDF (`.pdf`)
- DOCX (`.docx`)
- Word (`.doc`)
- Text (`.txt`)
- LaTeX (`.tex`)
- Images (`.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`)

---

#### Get Uploaded File

**Endpoint:** `GET /upload/{filename}`

**Response:** Binary file data

---

#### Delete Uploaded File

**Endpoint:** `DELETE /upload/{filename}`

**Response:**
```json
{
  "message": "File deleted successfully"
}
```

---

#### Upload Temporary File

**Endpoint:** `POST /upload/temp`

**Response:**
```json
{
  "message": "Temporary file uploaded successfully",
  "filename": "temp123.pdf",
  "file_path": "tmp/temp123.pdf"
}
```

---

#### Delete Temporary File

**Endpoint:** `DELETE /temp/{filename}`

**Response:**
```json
{
  "message": "Temporary file deleted successfully"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing the issue"
}
```

### HTTP Status Codes

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

### Common Errors

**400 Bad Request:**
```json
{
  "detail": "Email already registered"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden:**
```json
{
  "detail": "Not authorized to access this resource"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

---

## Rate Limiting

Currently, there are no rate limits implemented. Future versions may include rate limiting to prevent abuse.

## Versioning

The API is currently at version 1 (implied). Future versions may use URL versioning:
```
/api/v1/...
```

## Pagination

Pagination is not currently implemented. Future versions may include pagination for list endpoints.

## Response Formats

All responses are in JSON format unless otherwise specified (e.g., file downloads).

## Support

For API issues, please open an issue on the GitHub repository.
