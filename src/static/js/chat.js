document.addEventListener("DOMContentLoaded", () => {
  const conversationList = document.querySelector('.conversation-list');
  const messagesContainer = document.querySelector('.messages-container');
  const messageInputField = document.querySelector('.message-input input');
  const sendButton = document.querySelector('.send-btn');
  const newChatBtn = document.querySelector('.new-chat-btn');

  let currentConversationId = null;

  function formatTime(isoTime) {
    const date = new Date(isoTime);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function createConversationItem(convo) {
    const item = document.createElement('div');
    item.classList.add('conversation-item');
    item.dataset.id = convo.id;

    const name = convo.name || "Unnamed Conversation";
    const time = formatTime(convo.updated_at);

    item.innerHTML = `
      <div class="conversation-info">
        <div class="conversation-name" contenteditable="false">${name}</div>
        <div class="conversation-time">${time}</div>
      </div>
      <div class="conversation-actions">
        <button class="menu-btn"><i class="fas fa-ellipsis-h"></i></button>
        <div class="dropdown-menu">
          <button class="rename-btn">Rename</button>
          <button class="delete-btn">Delete</button>
        </div>
      </div>
    `;

    setupMenuBehavior(item);
    setupRenameEvent(item);
    setupDeleteEvent(item);

    item.addEventListener('click', (e) => {
      if (e.target.closest('.conversation-info')) {
        document.querySelectorAll('.conversation-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');
        currentConversationId = convo.id;
        loadMessages(convo.id);
      }
    });

    return item;
  }

  function setupMenuBehavior(item) {
    const menuBtn = item.querySelector('.menu-btn');
    const dropdownMenu = item.querySelector('.dropdown-menu');
    menuBtn.addEventListener('click', e => {
      dropdownMenu.classList.toggle('active');
      e.stopPropagation();
    });
    document.addEventListener('click', e => {
      if (!item.contains(e.target)) dropdownMenu.classList.remove('active');
    });
  }

  function setupRenameEvent(item) {
    const nameElem = item.querySelector('.conversation-name');
    const renameBtn = item.querySelector('.rename-btn');
    const convId = item.dataset.id;
    let oldName = nameElem.textContent.trim();

    renameBtn.addEventListener('click', e => {
      e.stopPropagation();
      nameElem.setAttribute('contenteditable', 'true');
      nameElem.classList.add('editing');
      nameElem.focus();
      const range = document.createRange();
      range.selectNodeContents(nameElem);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    });

    nameElem.addEventListener('blur', () => {
      nameElem.setAttribute('contenteditable', 'false');
      nameElem.classList.remove('editing');
      nameElem.textContent = oldName;
    });

    nameElem.addEventListener('keydown', async e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const newName = nameElem.textContent.trim() || "Unnamed Conversation";
        oldName = newName;
        nameElem.setAttribute('contenteditable', 'false');
        nameElem.classList.remove('editing');
        try {
          const res = await fetch('/api/chat/conversations', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: convId, name: newName, messages: [] })
          });
          const result = await res.json();
          if (!res.ok) {
            alert("Rename failed: " + (result.detail || result.message));
            nameElem.textContent = oldName;
          }
        } catch {
          alert("An error occurred while renaming.");
          nameElem.textContent = oldName;
        }
      }
    });
  }

  function setupDeleteEvent(item) {
    const deleteBtn = item.querySelector('.delete-btn');
    const convId = item.dataset.id;

    deleteBtn.addEventListener('click', async e => {
      e.stopPropagation();
      if (!confirm("Are you sure you want to delete this conversation?")) return;
      try {
        const res = await fetch(`/api/chat/conversations/${convId}`, { method: 'DELETE' });
        const result = await res.json();
        if (res.ok) {
          item.remove();
          if (convId === currentConversationId) {
            currentConversationId = null;
            messagesContainer.innerHTML = '';
          }
        } else {
          alert("Delete failed: " + (result.detail || result.message));
        }
      } catch {
        alert("An error occurred while deleting.");
      }
    });
  }

  async function loadConversations() {
    document.querySelectorAll('.conversation-item').forEach(el => el.remove());

    try {
      const res = await fetch("/api/chat/");
      if (!res.ok) throw new Error();
      const data = await res.json();

      const sortedConvos = data.conversations.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

      const newChatBtn = document.getElementById('new-chat-button');
      sortedConvos.forEach(c => {
        const item = createConversationItem(c);
        conversationList.insertBefore(item, newChatBtn);
      });

    } catch {
      console.error("Failed to load conversations");
    }
  }


  async function loadMessages(conversationId) {
    messagesContainer.innerHTML = '';
    try {
      const res = await fetch(`/api/chat/conversations/${conversationId}`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      data.messages.forEach(msg => messagesContainer.appendChild(createMessageElement(msg)));
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } catch {
      alert("Cannot load messages.");
    }
  }

  function createMessageElement(message) {
    const div = document.createElement('div');
    div.classList.add('message', message.role === 'user' ? 'sent' : 'received');
    div.innerHTML = `
      <div class="avatar"><i class="fas fa-${message.role === 'user' ? 'user' : 'robot'}"></i></div>
      <div class="message-content">
        <div class="message-text">${message.content}</div>
      </div>
    `;
    return div;
  }

  async function sendMessage() {
    const userMessage = messageInputField.value.trim();
    if (!userMessage) return;

    messagesContainer.innerHTML = '';

    messagesContainer.appendChild(createMessageElement({ role: 'user', content: userMessage }));
    messagesContainer.appendChild(createMessageElement({ role: 'bot', content: "This is a default bot response." }));
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    const payload = {
      id: currentConversationId ? currentConversationId : null,
      name: currentConversationId ? null : "New Conversation",
      messages: [
        { role: 'user', content: userMessage },
        { role: 'chatbot', content: "This is a default bot response." }
      ]
    };

    try {
      const res = await fetch('/api/chat/conversations', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error();

      const result = await res.json();

      if (!currentConversationId && result.id) {
        currentConversationId = result.id;
      }

      await loadConversations();

      document.querySelectorAll('.conversation-item').forEach(el => el.classList.remove('active'));
      const newItem = document.querySelector(`.conversation-item[data-id="${currentConversationId}"]`);
      if (newItem) {
        newItem.classList.add('active');
        loadMessages(currentConversationId);
      }

    } catch (e) {
      alert("Failed to save messages.");
    }

    messageInputField.value = '';
  }

  newChatBtn.addEventListener('click', () => {
    currentConversationId = null;
    messagesContainer.innerHTML = `
          <div class="messages-container" id="messagesContainer">
        <div class="empty-placeholder">How can I help you?</div>
      </div>
    `;

    document.querySelectorAll('.conversation-item').forEach(el => el.classList.remove('active'));
    messageInputField.value = '';
  });

  messageInputField.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
  });
  sendButton.addEventListener('click', sendMessage);

  loadConversations();
});
