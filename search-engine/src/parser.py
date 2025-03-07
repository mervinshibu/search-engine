import xml.etree.ElementTree as ET
from collections import namedtuple, OrderedDict
import os

# Define document and query types
Document = namedtuple('Document', ['doc_id', 'title', 'author', 'text'])
Query = namedtuple('Query', ['query_id', 'original_id', 'text'])

class CranfieldParser:
    """Parser for the Cranfield collection in TREC XML format."""
    
    @staticmethod
    def read_and_fix_xml(xml_file_path):
        """
        Read XML file and fix it by adding a root element if needed.
        
        Args:
            xml_file_path (str): Path to the XML file
            
        Returns:
            str: Valid XML content with a root element
        """
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if the content already has a root element
            if not content.strip().startswith('<?xml') and not content.strip().startswith('<xml>'):
                # Wrap the content with a root element
                content = f'<xml>\n{content}\n</xml>'
                
            return content
        except Exception as e:
            print(f"Error reading XML file: {e}")
            return None
    
    @staticmethod
    def parse_documents(xml_file_path):
        """
        Parse the Cranfield document collection.
        
        Args:
            xml_file_path (str): Path to the XML file containing documents
            
        Returns:
            list: List of Document objects
        """
        documents = []
        
        try:
            # Read and fix XML content
            xml_content = CranfieldParser.read_and_fix_xml(xml_file_path)
            if not xml_content:
                return []
                
            # Parse the fixed XML content
            root = ET.fromstring(xml_content)
            
            for doc_elem in root.findall('.//doc'):
                doc_id = doc_elem.find('docno').text.strip()
                
                # Extract title (may be None)
                title_elem = doc_elem.find('title')
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                
                # Extract author (may be None)
                author_elem = doc_elem.find('author')
                author = author_elem.text.strip() if author_elem is not None and author_elem.text else ""
                
                # Extract text content
                text_elem = doc_elem.find('text')
                text = text_elem.text.strip() if text_elem is not None and text_elem.text else ""
                
                # Combine title and text for indexing
                full_text = f"{title} {text}"
                
                documents.append(Document(doc_id, title, author, full_text))
                
            return documents
            
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return []
        except Exception as e:
            print(f"Error processing documents: {e}")
            return []
    
    @staticmethod
    def parse_queries(xml_file_path):
        """
        Parse the Cranfield queries.
        
        Args:
            xml_file_path (str): Path to the XML file containing queries
            
        Returns:
            list: List of Query objects with sequential IDs (1 to N)
            dict: Mapping between sequential IDs and original IDs
        """
        queries = []
        id_mapping = {}  # Maps sequential_id -> original_id
        
        try:
            # Read and fix XML content
            xml_content = CranfieldParser.read_and_fix_xml(xml_file_path)
            if not xml_content:
                return [], {}
            
            # Parse the fixed XML content
            root = ET.fromstring(xml_content)
            
            # First pass: collect all topics
            topics = []
            for topic_elem in root.findall('.//top'):
                original_id = topic_elem.find('num').text.strip()
                
                # Extract title (query text)
                title_elem = topic_elem.find('title')
                query_text = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                
                topics.append((original_id, query_text))
            
            # Second pass: assign sequential IDs
            for sequential_id, (original_id, query_text) in enumerate(topics, 1):
                id_mapping[sequential_id] = original_id
                queries.append(Query(str(sequential_id), original_id, query_text))
            
            print(f"Parsed {len(queries)} queries with sequential IDs (original IDs from {topics[0][0]} to {topics[-1][0]})")
            
            return queries, id_mapping
            
        except ET.ParseError as e:
            print(f"Error parsing query XML file: {e}")
            return [], {}
        except Exception as e:
            print(f"Error processing queries: {e}")
            return [], {}
    
    @staticmethod
    def parse_qrels(qrels_file_path):
        """
        Parse the relevance judgments file.
        
        Args:
            qrels_file_path (str): Path to the TREC-format qrels file
            
        Returns:
            dict: Dictionary mapping (query_id, doc_id) to relevance score
        """
        qrels = {}
        
        try:
            with open(qrels_file_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    
                    if len(parts) != 4:
                        continue
                        
                    query_id, iteration, doc_id, relevance = parts
                    
                    # Convert to integers
                    query_id = query_id.strip()
                    doc_id = doc_id.strip()
                    relevance = int(relevance)
                    
                    qrels[(query_id, doc_id)] = relevance
                    
            return qrels
            
        except Exception as e:
            print(f"Error parsing qrels file: {e}")
            return {}