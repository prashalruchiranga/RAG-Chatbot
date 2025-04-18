from langchain_core.documents import Document
from typing import List
import fitz


class PDFProcessor:
    def __init__(self, files: List):
        self.files = files

    def convert_pdf_to_documents(self, file) -> List[Document]:
        '''
        Convert an in-memory PDF file to a list of LangChain Document objects.
        '''
        file_bytes = file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        documents = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            metadata = {
                "source": getattr(file, "filename", "in-memory"),
                "page": page_num
            }
            documents.append(Document(page_content=text, metadata=metadata))
        return documents

    async def process_all_pdfs(self) -> List[Document]:
        '''
        Process all in-memory PDFs and return a flat list of Document objects.
        '''
        all_documents = []
        for file in self.files:
            documents = self.convert_pdf_to_documents(file)
            all_documents.extend(documents)
        return all_documents
    
    # async def load_pdf(self, pdf_path: Path):
    #     loader = PyPDFLoader(str(pdf_path))
    #     pages = []
    #     async for page in loader.alazy_load():
    #         pages.append(page)
    #     return pages
    
    # def save_to_txt(self, pages: List[Document], txt_path: Path):
    #     lines = [page.page_content for page in pages]
    #     content = "\n".join(lines)
    #     with open(txt_path, "w", encoding="utf-8") as f:
    #         f.write(content)

    # async def process_pdf(self, pdf_path: Path):
    #     txt_path = pdf_path.with_suffix(".txt")
    #     pages = await self.load_pdf(pdf_path)
    #     self.save_to_txt(pages, txt_path)

    # async def process_pdfs_in_directory(self):
    #     pdf_paths = list(self.data_directory.glob("*.pdf"))  
    #     tasks = [self.process_pdf(pdf) for pdf in pdf_paths]
    #     await asyncio.gather(*tasks)

    # def load_txts_in_directory(self):
    #     loader = DirectoryLoader(
    #         str(self.data_directory), 
    #         glob="*.txt", 
    #         loader_cls=TextLoader, 
    #         use_multithreading=True
    #     )
    #     return loader.load()
    