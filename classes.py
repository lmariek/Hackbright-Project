"""FACTORY OF FORM OBJECTS."""

from textblob import TextBlob
import re
from datetime import datetime


class Complaint(TextBlob):
    def __init__(self, decoded_text):
        super(Complaint, self).__init__(decoded_text)

        self.word_list = self.split()
        self.sentence_list = self.sentences
        self.plaintiff_fname = self.get_plaintiff_fname()
        self.plaintiff_lname = self.get_plaintiff_lname()
        self.case_no = self.get_case_no()
        self.county = self.get_county()
        self.state = self.get_state()
        self.defendant_fname = self.get_defendant_fname()
        self.defendant_lname = self.get_defendant_lname()
        self.defendant_residence = self.get_defendant_residence()
        self.amount_claimed = self.get_amount_claimed()
        self.claim = self.get_claim()
        self.counsel_fname = self.get_counsel_fname()
        self.counsel_lname = self.get_counsel_lname()
        self.counsel_firm = self. get_counsel_firm()
        self.complaint_date = self.get_complaint_date()
        self.legal_basis = self.get_legal_basis()
        # self.injury_date = self.get_injury_date()
        # self.injury_location = self.get_injury_location()
        # self.injury_description = self.get_injury_description()

        # etc...

# FIXME: refactor option to consolidate double ifs in one line, and return the self. (no name)
# FIXME: remove punctuation from word list so can not hardcode that into checks
# FIXME: .correct() everything that comes out
# FIXME: a way to grab other defendants and/or check if company or person

    # Could also check if what comes after starts with upper case, and if so pull it
    def get_plaintiff_fname(self):
        """Return the plaintiff's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Plaintiff':
                plaintiff_fname = self.word_list[i + 1]
                return plaintiff_fname.capitalize()


    def get_plaintiff_lname(self):
        """Return the plaintiff's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Plaintiff':
                plaintiff_lname = self.word_list[i + 3]
                return plaintiff_lname.capitalize()

    # FIXME: add a case number to template
    def get_case_no(self):
        """Return the plaintiff's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Case':
                if self.word_list[i + 1] == 'No.2':
                    case_no = self.word_list[i + 2]
                    return int(case_no)


    def get_county(self):
        """Return the county."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'COUNTY':
                if self.word_list[i + 1] == 'OF':
                    county = self.word_list[i + 2]
                    return county.capitalize()


    def get_state(self):
        """Return the state."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'STATE':
                if self.word_list[i + 1] == 'OF':
                    state = self.word_list[i + 2]
                    return state.capitalize()


    def get_defendant_fname(self):
        """Return the defendant's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'defendant':
                return self.word_list[i + 1]


    def get_defendant_lname(self):
        """Return the defendant's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'defendant':
                return self.word_list[i + 2]


    def get_amount_claimed(self):
        """Return the dollar of damages requested."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Amount':
                if self.word_list[i + 1] == 'claimed:':
                    return self.word_list[i + 2]


    def get_claim(self):
        """Return the type of claim as either the default PI or an error message."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('Personal Injury'):
                return 'Personal Injury'
            else:
                return 'UNKNOWN'


    def get_legal_basis(self):
        """Return the types of legal claims made in the complaint.

        FIXME: add other types of claims here."""

        result = []

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('Negligence') and 'Negligence' not in result:
                result.append('Negligence')
            # etc.
        result = ' '.join(result)

        return result


    def get_defendant_residence(self):
        """Return the defendant's city, county, state of residence."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'resides':
                defendant_residence = self.word_list[i + 2:i + 6]
                result = ' '.join(defendant_residence)
                return result[:-1]


    def get_counsel_fname(self):
        """Return the opposing counsel's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'P.C.':
                return self.word_list[i + 2]


    def get_counsel_lname(self):
        """Return the opposing counsel's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'P.C.' or self.word_list[i] == 'LLC':
                return self.word_list[i + 4]


    def get_counsel_firm(self):
        """Return the opposing counsel's firm name."""

        firm = self.sentence_list[-3]
        return firm.title()


    def get_complaint_date(self):
        """Stampe the complaint with the date processed."""

        return datetime.utcnow()


    def get_injury_date(self):

        return 'N/A'

        # regex: 'On *** plaintiff was'


    def get_injury_location(self):

        return 'N/A'


    def get_injury_description(self):

        return 'N/A'

class Answer(TextBlob):
    pass 