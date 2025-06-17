from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.auto import partition

file_path = "D:/miscellaneous/wells_stuff/doc_chunk_copy/input_files"
base_file_name = "scanned_doc"

def main():
    print("Starting........")
    filename=f"{file_path}/{base_file_name}.pdf"
    elements = partition_pdf(filename=filename, strategy="auto")
    print("partition completed, starting chunking.......")

    chunks = chunk_by_title(elements)
    print("chunking completed, printing chunks.....")
    for chunk in chunks:
        print(chunk)
        print("\n\n" + "-"*80)
        input()
    
    print("finished")

if __name__ == "__main__":
    main()