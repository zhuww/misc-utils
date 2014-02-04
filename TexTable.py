def alphabet():
    alphabetlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for value in alphabetlist:
        yield value

InputError = 'Mismatch:'

class deluxetable:

    def alphabet(self):
        alphabetlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for value in alphabetlist:
            self.commentslines += '\\tablenotetext{%s}{%s}\n' % (value, self.comments.next())
            #print '\tablenotetext{%s}{%s}' % (value, self.comments.next())
            yield value

    def __init__(self, Caption='', colsetting='', colnames=[], data=[], comments=[],label='',extra='', rotate=False):
        if colnames == []: raise InputError, 'must have column names specified!'
        if data == []: raise InputError, 'must have data provided!'
        if not len(colnames) == len(data):
            raise InputError, 'number of column names does match number of columns in the data!'
        elif not colsetting == '' and not len(colsetting) == len(colnames):
            raise InputError, 'number of control characters in the colsetting does not match number of columns'
        elif colsetting == '':
            colsetting = 'c' * len(colnames)
        else:pass
        if rotate:
            rotation = '\\rotate'
        else:
            rotation = ''


        self.comments = iter(comments)
        self.commentslines = ''
        cols=''
        abc = self.alphabet()
        while not Caption.find('#') == -1:
            i = Caption.find('#')
            if Caption[i-1] == '\\':
                Captioni = Caption.replace('#',r'@TexTableSpecialMarker@', 1)
                continue
            Caption = Caption.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)
        for name in colnames:
            while not name.find('#') == -1:
                i = name.find('#')
                if name[i-1] == '\\':
                    name = name.replace('#',r'@TexTableSpecialMarker@', 1)
                    continue
                name = name.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)
            cols += '\colhead{%s}  &' % name
        cols = cols[:-1]
        rowcounts = len(data[0])
        colcounts = len(data)
        datalines = []
        for row in range(rowcounts):
            datarow = str(data[0][row])
            for col in range(1,colcounts):
                datarow += '&  ' + str(data[col][row])
            datalines.append(datarow)
        datatable = '\\\\\n'.join(datalines)
        while not datatable.find('#') == -1:
                i = datatable.find('#')
                if datatable[i-1] == '\\':
                    datatable = datatable.replace('#',r'@TexTableSpecialMarker@', 1)
                    continue
                datatable = datatable.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)



        self.parsestring = r"""
\clearpage
\begin{deluxetable}{%(colsetting)s}
%(rotation)s
\tabletypesize{\footnotesize}
\tablewidth{0pt}
\tablecaption{\label{%(label)s} %(Caption)s }
\tablehead{ %(colnames)s }
\startdata
%(data)s
\enddata
%(comments)s
%(extra)s
\end{deluxetable}

\clearpage """ % {'label':label, 'colsetting':colsetting, 'Caption':Caption, 'colnames':cols, 'data':datatable, 'comments':self.commentslines, 'extra':extra, 'rotation':rotation}
        self.parsestring = self.parsestring.replace(r'@TexTableSpecialMarker@', '#')


    def __str__(self):
        return self.parsestring

#x = alphabet()
#print '%s %s %s %s %s' % x
