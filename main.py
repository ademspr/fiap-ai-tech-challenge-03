import glob
import xml.etree.ElementTree as ET

import pandas as pd

qa = []
for file_path in glob.glob("data/**/*.xml", recursive=True):
    xml = ET.parse(file_path)
    root = xml.getroot()

    if focus := root.findtext('./Focus'):
        source = root.get('source')
        url = root.get('url')

        for qa_pair in root.findall('./QAPairs/QAPair'):
            question = qa_pair.findtext('./Question')
            answer = qa_pair.findtext('./Answer')

            if answer:
                qa.append({
                    'source': source,
                    'url': url,
                    'focus': focus,
                    'question': question,
                    'answer': answer
                })

df = pd.DataFrame(qa)
df.info()
