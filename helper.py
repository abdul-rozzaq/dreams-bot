from googletrans import Translator
import requests

translator = Translator()



def translate(text: str, dest: str = 'en', src: str = 'auto',) -> str:
    return translator.translate(text, dest=dest, src=src).text


class Dream:
    def __init__(self, id: int, title: str, meaning: str, author: str) -> None:
        self.id, self.author = id, author
        self.title, self.meaning = translate(f"{title} ~ {meaning}", 'uz').split('~')
        
    @staticmethod
    def fromString(body):
        body, map = body.strip(), {}

        start, end, key, valueStart = None, None, None, None

        
        for index in range(len(body)):
            char = body[index]

            if char == "[":
                start = index + 1
            
            elif char == "]":
                end = index
                
                
            if start is not None and end is not None:
                key = body[start:end]
                start, end, valueStart = None, None, end + 1
                
            
            if char == "[" and valueStart is not None:
                map[key] = body[valueStart:index].replace('=>', '').strip()
        
            

        return Dream(map['id'], map['title'], map['meaning'], map['author'])
        
        
        

    def __str__(self) -> str:
        return f"Dream({self.id},{self.title},{self.meaning[:20]},{self.author})"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Dream) and self.id == __value.id


def getMeans(text) -> list[Dream]:
    
    text = translate(text, src='uz')
    
    print(text)
    
    url = f'https://www.myislamicdream.com/search.php?txtSearch={text}'

    response = requests.get(url)

    body = response.text.replace('<br>', '\n')
    
    body = body[body.index('<!--')+4:body.index('-->')]
    
    return [Dream.fromString(dream.replace('(', '').replace(')', '')) for dream in body.split('Array')[1:]]


