# User Guide

## Getting Started

### Login

1. Navigate to the Protein Lab application
2. Use the sidebar to login with your credentials
3. Different roles have different permissions:
   - **Viewer**: Read-only access
   - **Researcher**: Can add and modify proteins
   - **Admin**: Full access including deletion

## Features

### Browse Proteins

Navigate to the **Proteins** page to view all proteins in the database.

- Search by name, UniProt ID, or gene name
- Filter by validation status
- View detailed protein information
- Access version history

### Add New Protein

Navigate to the **Add Protein** page.

1. Fill in required fields:
   - UniProt ID
   - Protein Name
   - Sequence
   - Organism

2. Optional fields:
   - Gene name, family, function
   - PDB ID, EC number
   - Molecular weight, location
   - Keywords

3. Click **Add Protein**

**Quick Import:**
- Fetch from UniProt by entering UniProt ID
- Fetch from PDB by entering PDB ID

### Advanced Search

Navigate to the **Search** page for advanced filtering:

- Text search across multiple fields
- Filter by organism, family, gene name
- Length range filtering
- PDB structure availability
- Validation status
- Post-translational modifications

### AI Assistant

Navigate to the **AI Assistant** page to use natural language queries:

**Examples:**
- "Show me all human proteins"
- "Find kinases longer than 500 amino acids"
- "Which proteins have PDB structures?"

The AI will:
1. Convert your question to SQL
2. Show you the generated query
3. Let you execute or modify it

### Analytics Dashboard

Navigate to the **Analytics** page to view:

- Database statistics
- Protein distribution by organism
- Family distribution
- Sequence length distribution
- Monthly additions trend
- Data quality metrics

### Sequence Analysis

Navigate to the **Sequence Analysis** page for:

**BLAST Search:**
- Search for similar sequences
- Set E-value threshold
- Choose database (Local, UniProt, PDB)

**Sequence Alignment:**
- Multiple sequence alignment
- Choose method (ClustalW, MUSCLE, T-Coffee)

**Motif Detection:**
- Search for PROSITE patterns
- Identify Pfam domains
- SMART domains
- InterPro entries

**Properties Calculator:**
- Length and molecular weight
- Isoelectric point
- Hydrophobicity
- Instability index

### 3D Structure Viewer

Navigate to the **Structure Viewer** page to:

- View 3D protein structures
- Choose from database proteins
- Upload PDB files
- Fetch from RCSB PDB
- Customize display (cartoon, stick, sphere, surface)
- Color by chain, atom type, or secondary structure
- Interactive rotation and zoom

### Batch Upload

Navigate to the **Batch Upload** page to:

1. **Download template** (CSV or Excel)
2. **Fill in protein data** following the template
3. **Upload file**
4. **Review validation** results
5. **Import proteins**

Options:
- Validate sequences
- Check for duplicates
- Verify UniProt IDs
- Auto-fetch missing data

### Export Data

Navigate to the **Export** page to download data:

**Export Options:**
- All proteins
- Filtered selection
- Specific proteins (comma-separated IDs)

**Formats:**
- FASTA
- CSV
- Excel
- JSON
- GenBank
- XML

**Additional Options:**
- Include version history
- Include audit logs
- Compress as ZIP

## Best Practices

### Data Quality

1. Always validate sequences before importing
2. Use standard amino acid codes
3. Include UniProt IDs when available
4. Add functional descriptions
5. Link to PDB structures when possible

### Collaboration

1. Use appropriate role permissions
2. Add meaningful change descriptions when updating
3. Review audit logs for tracking changes
4. Export backups regularly

### Search Tips

1. Use wildcards (*) for partial matches
2. Combine multiple filters for precise results
3. Save frequently used search queries
4. Use the AI assistant for complex queries

## Troubleshooting

### Cannot Login

- Check username and password
- Verify account is active
- Contact admin for password reset

### Upload Fails

- Check file format (CSV or XLSX)
- Verify required columns are present
- Ensure sequences are valid
- Check for duplicate UniProt IDs

### Export Not Working

- Check you have permission
- Verify selection is not empty
- Try smaller data sets for large exports

### Search Returns No Results

- Check spelling
- Remove overly restrictive filters
- Use broader search terms
- Try the AI assistant

## Support

For issues or questions:
1. Check this user guide
2. Review API documentation
3. Contact your system administrator
4. Open an issue on GitHub
