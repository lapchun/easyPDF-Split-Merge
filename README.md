# easyPDF-Split-Merge
A **single python file** to split and merge multiple pdf files.

## Usage
* Download this repository.
* Modify the config file like this (`config.txt`):

```
D:/my_folder/my_pdf_1.pdf 1-10,16,22
D:/my_folder/my_pdf_2.pdf 1-40
D:/my_folder/my_pdf_3.pdf 6,8,9-20
```
* Run the python file `pdf_split_merge.pdf`.

## Note
* The `config.txt` must be in the same directory with this python file，or you should provide the absolute path of the config.txt.
* The content of the `config.txt` must use the **forward slash "/"** instead of the back slash "\\".
* The `new.pdf` will be saved in the same directory in default.
* Plus, the name and path of `*.txt` and `*.pdf` depend on you.

### This project is forked from [gaborvecsei/Pdf-Split-Merge](https://github.com/gaborvecsei/Pdf-Split-Merge) and improved.
