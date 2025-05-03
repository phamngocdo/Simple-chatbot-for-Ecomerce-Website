document.addEventListener("DOMContentLoaded", () => {
  const conversationList = document.querySelector('.conversation-list');
  const messagesContainer = document.querySelector('.messages-container');
  const messageInput = document.getElementById('message-input');
  const sendBtn = document.getElementById('send-btn');

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
      </div>
      <div class="conversation-actions">
        <button class="menu-btn"><i class="fas fa-ellipsis-h"></i></button>
        <div class="dropdown-menu">
          <button class="rename-btn">Rename</button>
          <button class="delete-btn">Delete</button>
        </div>
      </div>
      <div class="time">${time}</div>
    `;

    setupMenuBehavior(item);
    setupRenameEvent(item);
    setupDeleteEvent(item);

    item.addEventListener('click', () => {
      currentConversationId = convo.id;
      loadMessages(convo.id);
    });

    return item;
  }

  function setupMenuBehavior(item) {
    const menuBtn = item.querySelector('.menu-btn');
    const dropdownMenu = item.querySelector('.dropdown-menu');

    menuBtn.addEventListener('click', (e) => {
      dropdownMenu.classList.toggle('active');
      e.stopPropagation();
    });

    document.addEventListener('click', (e) => {
      if (!item.contains(e.target)) {
        dropdownMenu.classList.remove('active');
      }
    });
  }

  function setupRenameEvent(item) {
    const nameElem = item.querySelector('.conversation-name');
    const renameBtn = item.querySelector('.rename-btn');
    const convId = item.dataset.id;
    let oldName = nameElem.textContent.trim();

    renameBtn.addEventListener('click', () => {
      nameElem.setAttribute('contenteditable', 'true');
      nameElem.classList.add('editing');
      nameElem.focus();
      const range = document.createRange();
      const sel = window.getSelection();
      range.selectNodeContents(nameElem);
      sel.removeAllRanges();
      sel.addRange(range);
    });

    nameElem.addEventListener('blur', () => {
      nameElem.setAttribute('contenteditable', 'false');
      nameElem.classList.remove('editing');
      nameElem.textContent = oldName;
    });

    nameElem.addEventListener('keydown', async (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const newName = nameElem.textContent.trim();
        if (!newName) {
          nameElem.textContent = "Unnamed Conversation";
          return;
        }

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
        } catch (error) {
          console.error("Rename error:", error);
          alert("An error occurred while renaming.");
          nameElem.textContent = oldName;
        }
      }
    });
  }

  function setupDeleteEvent(item) {
    const deleteBtn = item.querySelector('.delete-btn');
    const convId = item.dataset.id;

    deleteBtn.addEventListener('click', async () => {
      if (!confirm("Are you sure you want to delete this conversation?")) return;

      try {
        const res = await fetch(`/api/chat/conversations/${convId}`, {
          method: 'DELETE'
        });

        const result = await res.json();
        if (!res.ok) {
          alert("Delete failed: " + (result.detail || result.message));
          return;
        }

        item.remove();
      } catch (error) {
        console.error("Delete error:", error);
        alert("An error occurred while deleting.");
      }
    });
  }

  async function loadConversations() {
    try {
      const res = await fetch("/api/chat/");
      if (!res.ok) throw new Error("Failed to fetch conversations");

      const data = await res.json();
      if (!Array.isArray(data.conversations)) {
        throw new Error("Expected conversations array");
      }

      data.conversations.forEach(c => {
        const item = createConversationItem(c);
        conversationList.appendChild(item);
      });
    } catch (err) {
      console.error("Error loading conversations:", err);
    }
  }

  async function loadMessages(conversationId) {
    try {
      const res = await fetch(`/api/chat/conversations/${conversationId}`);
      const data = await res.json();

      if (!data.messages || !Array.isArray(data.messages)) {
        throw new Error("Invalid message data");
      }

      messagesContainer.innerHTML = '';
      data.messages.forEach(m => {
        messagesContainer.appendChild(createMessageElement(m));
      });
    } catch (err) {
      console.error("Error loading messages:", err);
    }
  }

  function createMessageElement(message) {
    const div = document.createElement('div');
    div.classList.add('message', message.role === 'user' ? 'sent' : 'received');

    const avatar = document.createElement('div');
    avatar.classList.add('avatar');
    avatar.innerHTML = message.role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

    const content = document.createElement('div');
    content.classList.add('message-content');

    const text = document.createElement('div');
    text.classList.add('message-text');
    text.textContent = message.content;

    content.appendChild(text);
    div.appendChild(avatar);
    div.appendChild(content);
    return div;
  }


  loadConversations();
});
