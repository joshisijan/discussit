from django.db import models
from django.contrib.auth.models import User

vote_category = (
    ('question','question'),
    ('answer','answer'),
)

vote_type = (
    ('upvote','upvote'),
    ('downvote','downvote'),
)

class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return str(self.name)
    
class Question(models.Model):
    title = models.TextField()
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    verefied = models.BooleanField(default = 0)
    seen = models.BooleanField(default = 0)

    def __str__(self):
        return str(self.creator) + "-->" + str(self.title)

    def get_no_of_votes(self):
        topic = Vote.objects.filter(question = self)
        topic = topic.filter(what = 'upvote')
        topic = topic.exclude(voter = self.creator)
        up_votes = 0
        for topic in topic:
            up_votes += 1

        topic = Vote.objects.filter(question = self)
        topic = topic.filter(what = 'downvote')
        topic = topic.exclude(voter = self.creator)
        down_votes = 0
        for topic in topic:
            down_votes += 1
        votes = up_votes - down_votes
        return votes

    def get_answers(self):
        answer = Answer.objects.filter(question = self)
        answer = answer.exclude(creator = self.creator)
        answer = answer.order_by('-pub_date')
        return answer



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + "__" + str(self.question)
    
    def get_no_of_votes(self):
        topic = Vote.objects.filter(answer = self)
        topic = topic.filter(what = 'upvote')
        topic = topic.exclude(voter = self.creator)
        up_votes = 0
        for topic in topic:
            up_votes += 1

        topic = Vote.objects.filter(answer = self)
        topic = topic.filter(what = 'downvote')
        topic = topic.exclude(voter = self.creator)
        down_votes = 0
        for topic in topic:
            down_votes += 1
        votes = up_votes - down_votes
        return votes

class Vote(models.Model):
    what = models.CharField(choices=vote_type, max_length=50)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.what) +"__" +  str(self.voter) + "__" + str(self.question) + "__" + str(self.answer)
    
    

    
    