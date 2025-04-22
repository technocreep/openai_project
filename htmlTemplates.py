css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
img {
  border-radius: 50%;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://c02.purpledshub.com/uploads/sites/41/2024/10/ameca.jpg?w=1029&webp=1" style="border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.giantfreakinrobot.com/wp-content/uploads/2021/02/ben-stiller-simple-jack.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''