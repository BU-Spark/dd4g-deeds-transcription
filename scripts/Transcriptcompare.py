from collections import Counter

def compare_transcripts(chunk1, chunk2):
    chunk1_cleaned = chunk1.strip().lower().split()
    chunk2_cleaned = chunk2.strip().lower().split()

    chunk1_counter = Counter(chunk1_cleaned)
    chunk2_counter = Counter(chunk2_cleaned)

    matching_words_count = sum((chunk1_counter & chunk2_counter).values())
    total_words_chunk1 = len(chunk1_cleaned)
    total_words_chunk2 = len(chunk2_cleaned)
    if total_words_chunk1 == 0:
        matching_percentage = 0
    else:
        matching_percentage = (matching_words_count / total_words_chunk1) * 100


    non_matching_words_chunk1 = set(chunk1_cleaned) - set(chunk2_cleaned)
    non_matching_words_chunk2 = set(chunk2_cleaned) - set(chunk1_cleaned)


    result = {
        "matching_count": matching_words_count,
        "matching_percentage": matching_percentage,
        "non_matching_words_chunk1": non_matching_words_chunk1,
        "non_matching_words_chunk2": non_matching_words_chunk2
    }
    
    return result

chunk1 = """
    Fellow-Citizens of the Senate and of the House of Representatives: 
    Among the vicissitudes incident to life no event could have filled me with greater anxieties than that of which the notification was transmitted
     by your order, and received on the 14th day of the present month. On the one hand, I was summoned by my Country, 
    whose voice I can never hear but with veneration and love, from a retreat which I had chosen with the fondest predilection, and, in my flattering hopes, with an immutable decision, as the asylum of my declining years--a retreat which was rendered every day more necessary as well as more dear to me by the addition of habit to inclination, and of frequent interruptions in my health to the gradual waste committed on it by time. On the other hand, the magnitude and difficulty of the trust to which the voice of my country called me, being sufficient to awaken in the wisest and most experienced of her citizens a distrustful scrutiny into his qualifications, could not but overwhelm with despondence one who (inheriting inferior endowments from nature and unpracticed in the duties of civil administration) ought to be peculiarly conscious of his own deficiencies. In this conflict of emotions all I dare aver is that it has been my faithful study to collect my duty from a just appreciation of every circumstance by which it might be affected. All I dare hope is that if, in executing this task, I have been too much swayed by a grateful remembrance of former instances, or by an affectionate sensibility to this transcendent proof of the confidence of my fellow-citizens, and have thence too little consulted my incapacity as well as disinclination for the weighty and untried cares before me, my error will be palliated by the motives which mislead me, and its consequences be judged by my country with some share of the partiality in which they originated.
"""

chunk2 = """
Fellow-Citizens of the Senate and of the House of Representatives:
Among  the  vicissitudes  incident  to  life  no  event  could  have  filled  me  with  greater  anxieties  than
that of which the notification was transmitted by your order, and received on the 14th day of the present month. On the one hand, I was summoned by my Country, whose voice I can never hear
but with veneration and love, from a retreat which I had chosen with the fondest predilection, and,
in my flattering hopes, with an immutable decision, as the asylum of my declining years--a retreat which  was  rendered  every  day  more  necessary  as  well  as  more  dear  to  me  by  the  addition  of
habit to inclination, and of frequent interruptions in my health to the gradual waste committed on it
by time. On the other hand, the magnitude and difficulty of the trust to which the voice of my coun-
try called me, being sufficient to awaken in the wisest and most experienced of her citizens a dis-
trustful scrutiny into his qualifications, could not but overwhelm with despondence one who (inher-
iting inferior endowments from nature and unpracticed in the duties of civil administration) ought to
be peculiarly conscious of his own deficiencies. In this conflict of emotions all I dare aver is that it
has  been  my  faithful  study  to  collect  my  duty  from  a  just  appreciation  of  every  circumstance  by
which it might be affected. All I dare hope is that if, in executing this task, I have been too much
swayed  by  a  grateful  remembrance  of  former  instances,  or  by  an  affectionate  sensibility  to  this
transcendent proof of the confidence of my fellow-citizens, and have thence too little consulted my
incapacity  as  well  as  disinclination  for  the  weighty  and  untried  cares  before  me,  my  error  will  be
palliated by the motives which mislead me, and its consequences be judged by my country with
some share of the partiality in which they originated.
"""
result = compare_transcripts(chunk1, chunk2)
print(f"Number of matching words: {result['matching_count']}")
print(f"Percentage of matching words: {result['matching_percentage']:.2f}%")
print(f"Words in chunk1 that do not match: {result['non_matching_words_chunk1']}")
print(f"Words in chunk2 that do not match: {result['non_matching_words_chunk2']}")
