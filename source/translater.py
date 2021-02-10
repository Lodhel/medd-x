import boto3


class Translater:
    aws_secret_access_key= "kN+R/pTSz2C8cKQ83R7ICSmPt53qq2Wt/cFIqKZ9"
    aws_access_key_id = "AKIA5A6NLIUYXKOGMDUE"

    def translate(self, text, our_lang, your_lang):
        translate = boto3.client('translate', region_name='us-west-2',
                 aws_access_key_id=self.aws_access_key_id,
                 aws_secret_access_key=self.aws_secret_access_key)

        result = translate.translate_text(Text=text,
                                          SourceLanguageCode=our_lang,
                                          TargetLanguageCode=your_lang)

        return result["TranslatedText"]