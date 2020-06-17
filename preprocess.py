# coding=gbk
import os

from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
from word_to_vec import *


def pure_email(file_path):
    s_file_path = os.listdir(file_path)
    fail_file = []
    pure_email = []
    for i in range(len(s_file_path)):
        path = os.path.join(file_path, s_file_path[i])
        if os.path.isfile(path):
            try:
                fr = open(path, 'r', encoding='utf-8')
                fr_file = fr.readlines()
            except Exception as e:
                fail_file.append(path)
            else:
                pure_email1 = []
                for line in fr_file:
                    line = line.strip()
                    pure_email1.append(line)
                while "" in pure_email1:
                    pure_email1.remove('')

                pure_email.append(pure_email1)
    return pure_email, fail_file


def list2string(email_list):
    string_list = []
    for item in email_list:
        string = item[0] + ' ' + item[1]
        for index in range(1, len(item) - 1):
            string = string + ' ' + item[index + 1]
        string_list.append(string)
    return string_list


stopwords = ["a", "a's", "able", "about", "above", "according", "accordingly", "across", "actually", "after",
             "afterwards", "again", "against", "ain't", "all", "allow", "allows", "almost", "alone", "along", "already",
             "also", "although", "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow",
             "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate",
             "are", "aren't", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away",
             "awfully", "b", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
             "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both",
             "brief", "but", "by", "c", "c'mon", "c's", "came", "can", "can't", "cannot", "cant", "cause", "causes",
             "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently",
             "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn't",
             "course", "currently", "d", "definitely", "described", "despite", "did", "didn't", "different", "do",
             "does", "doesn't", "doing", "don't", "done", "down", "downwards", "during", "e", "each", "edu", "eg",
             "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever",
             "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f",
             "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former", "formerly",
             "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting", "given", "gives", "go",
             "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly", "has",
             "hasn't", "have", "haven't", "having", "he", "he's", "hello", "help", "hence", "her", "here", "here's",
             "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his", "hither",
             "hopefully", "how", "howbeit", "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "ignored",
             "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar",
             "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "j", "just",
             "k", "keep", "keeps", "kept", "know", "known", "knows", "l", "last", "lately", "later", "latter",
             "latterly", "least", "less", "lest", "let", "let's", "like", "liked", "likely", "little", "look",
             "looking", "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely",
             "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name", "namely", "nd",
             "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine",
             "no", "nobody", "non", "none", "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere",
             "o", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only",
             "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside",
             "over", "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus",
             "possible", "presumably", "probably", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re",
             "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "s",
             "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed",
             "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven",
             "several", "shall", "she", "should", "shouldn't", "since", "six", "so", "some", "somebody", "somehow",
             "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified",
             "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken", "tell",
             "tends", "th", "than", "thank", "thanks", "thanx", "that", "that's", "thats", "the", "their", "theirs",
             "them", "themselves", "then", "thence", "there", "there's", "thereafter", "thereby", "therefore",
             "therein", "theres", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think",
             "third", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru",
             "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying",
             "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon",
             "us", "use", "used", "useful", "uses", "using", "usually", "uucp", "v", "value", "various", "very", "via",
             "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've",
             "welcome", "well", "went", "were", "weren't", "what", "what's", "whatever", "when", "whence", "whenever",
             "where", "where's", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether",
             "which", "while", "whither", "who", "who's", "whoever", "whole", "whom", "whose", "why", "will", "willing",
             "wish", "with", "within", "without", "won't", "wonder", "would", "wouldn't", "x", "y", "yes", "yet", "you",
             "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "z", "zero"]
fr = open('stopwords.txt', encoding='utf-8')
signal_stopwords = []
for line in fr.readlines():
    signal_stopwords.append(line.strip())
signal_stopwords = signal_stopwords[:130]


# 解析html
class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def list2string(email_list):
    string_list = []
    for item in email_list:
        string = item[0] + ' ' + item[1]
        for index in range(1, len(item) - 1):
            string = string + ' ' + item[index + 1]
        string_list.append(string)
    return string_list


# 去停用词,解析html
def sanitiser_email(content):
    vocab_list = []
    for string in content:
        sanitiser_email = []
        text = dehtml(string)
        text = text.replace('\n', '')
        text = text.replace('\\n', '')
        text = text.split(' ')
        for item in text:
            item = item.lower()
            for signal in signal_stopwords:
                if signal in item:
                    item = item.replace(signal, '')
                    # print(signal)
            if item in stopwords:
                item = item.replace(item, '')
            sanitiser_email.append(item)

        string = sanitiser_email[0] + ' ' + sanitiser_email[1]
        # string = pure_email[0] + ' ' + pure_email[1]
        for index in range(1, len(sanitiser_email) - 1):
            string = string + ' ' + sanitiser_email[index + 1]
        # string.replace('  ', '')
        vocab_list.append(string)
    return vocab_list


def parse_email(email):
    count_url = 0
    count_atta = 0
    email_feature = [0, 0]
    for item in email:
        if ('<head>' in item) | ('<body>' in item):
            email_feature[0] = 1.0
        if ('<script>') in item:
            email_feature[1] = 1.0
        if ('http://') in item:
            count_url += 1.0
        if 'Content-Disposition: attachment' in item:
            count_atta += 1.0
    email_feature.append(float(count_url))
    email_feature.append(float(count_atta))
    return email_feature


def build_email_feature(pure_email, vec_feature):  # vec_feature是word2vec产生的特征值。
    email_feature = []
    for i in range(len(pure_email)):
        feature = parse_email(pure_email[i])
        feature.extend(list(vec_feature[i]))
        email_feature.append(feature)
    return email_feature


def build_train_word2vec(alldataDir_list):
    pureemail = []
    for dataDir in alldataDir_list:
        email, failemail = pure_email(dataDir)
        pureemail.extend(email)
    string_list = list2string(pureemail)
    model = word2vec_model(string_list, 100)
    return model


def create_feature(dataDir):
    email, fail_email = pure_email(dataDir)
    email_copy = email.copy()
    string_list = list2string(email_copy)
    vocab_list = sanitiser_email(string_list)
    wordvec = build_wordvec(vocab_list, 100)
    email_feature = build_email_feature(email, wordvec)


    return email_feature



