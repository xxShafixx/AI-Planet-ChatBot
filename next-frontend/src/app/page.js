'use client'
import Image from "next/image";
import { useState } from 'react';

export default function Home() {
  const [pdfUploaded, setPdfUploaded] = useState(false);
  const [documentId, setDocumentId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [fileName, setFileName] = useState('');

  const uploadPdf = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/upload', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
        },
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setPdfUploaded(true);
        setDocumentId(data.document_id);
        console.log("Upload successful:", data.message);
      } else {
        console.error("Upload failed:", data);
      }
    } catch (error) {
      console.error("Error uploading PDF:", error);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    if (!documentId) {
      alert('Please upload a PDF first.');
      return;
    }

    const question = inputValue.trim();

    // Add the user's question to messages
    setMessages((prevMessages) => [...prevMessages, { role: 'user', content: question }]);

    // Clear the input
    setInputValue('');

    // Add a placeholder assistant message with loading: true
    setMessages((prevMessages) => [...prevMessages, { role: 'assistant', loading: true }]);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/ask/${documentId}`, {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      if (response.ok) {
        const answer = data.answer;

        // Update the last message (placeholder) with the actual assistant's answer
        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          updatedMessages[updatedMessages.length - 1] = { role: 'assistant', content: answer };
          return updatedMessages;
        });
      } else {
        console.error('Failed to get answer:', data);
        // Remove the placeholder assistant message
        setMessages((prevMessages) => prevMessages.slice(0, -1));
      }
    } catch (error) {
      console.error('Error getting answer:', error);
      // Remove the placeholder assistant message
      setMessages((prevMessages) => prevMessages.slice(0, -1));
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="h-screen w-screen">
      {/* Header */}
      <div className="inline-flex items-center w-full bg-white h-[10%] drop-shadow-lg justify-between px-4 sm:px-16">
        <Image src="/logo.png" width={100} height={50} alt="logo" />
        <div>
          {pdfUploaded && (
            <div className="text-green-600 inline-flex px-8 text-sm font-semibold items-center gap-x-2">
              <div className="border border-green-600 rounded-md p-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="size-4"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
                  />
                </svg>
              </div>
              {fileName}
            </div>
          )}

          <input
            type="file"
            accept="application/pdf"
            onChange={uploadPdf}
            className="hidden"
            id="pdfUpload"
          />
          <label
            htmlFor="pdfUpload"
            className="cursor-pointer border-black border inline-flex gap-x-2 bg-white px-8 py-2 rounded-md hover:scale-105 transition"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="size-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
              />
            </svg>
            <div className="font-bold sm:visible invisible"> Upload PDF </div>
          </label>
        </div>
      </div>

      {/* Middle */}
      <div className="h-[80%] bg-white mt-4">

        {pdfUploaded ? (
          <div className="h-full overflow-y-auto">
            {messages.map((message, key) => (
              <div
                className={`w-full flex px-4 sm:px-16 items-start ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
                key={key}
              >
                {message.role === 'assistant' && (
                  <>
                    <Image
                      src="/ai_dp.png"
                      className="h-[48px] w-[48px] m-4"
                      height={48}
                      width={48}
                      alt="Assistant DP"
                    />
                    {message.loading ? (
                      // Display the loading animation
                      <div className="flex items-center h-full max-w-[70%] p-3 m-2 rounded-md">
                        <div className="flex space-x-1 text-sm">
                          <div className="h-8 w-4 rounded-full animate-bounce" style={{ animationDelay: '-0.3s' }}>
                            🔴
                          </div>
                          <div className="h-8 w-4 rounded-full animate-bounce" style={{ animationDelay: '-0.15s' }}>
                            🟡
                          </div>
                          <div className="h-8 w-4 rounded-full animate-bounce">
                            🔵
                          </div>
                        </div>
                      </div>
                    ) : (
                      // Display the assistant's message
                      <div className="flex items-center h-full max-w-[70%] p-3 m-2 rounded-md bg-gray-100 text-left">
                        {message.content}
                      </div>
                    )}
                  </>
                )}
                {message.role === 'user' && (
                  <>
                    <div className="flex items-center h-full max-w-[70%] p-3 m-2 rounded-md bg-blue-100 text-right">
                      {message.content}
                    </div>
                    <Image
                      src="/user_dp.png"
                      className="h-[48px] w-[48px] m-4"
                      height={48}
                      width={48}
                      alt="User DP"
                    />
                  </>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            Please upload the PDF to continue
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="flex items-center h-[10%] sm:px-16 mx-4">
        <div className="relative w-full">
          <input
            placeholder="Send a message..."
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="focus:bg-white font-medium focus:shadow outline-none text-[#6E7583] rounded-md bg-[#E4E8EE] w-full h-12 border-slate-300 border px-4 pr-10"
          />
          <svg
            onClick={sendMessage}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="absolute right-3 top-1/2 transform -translate-y-1/2 w-6 h-6 text-gray-500 cursor-pointer"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 12L3.269 3.125A59.769 59.769 0 0121.485 12 59.768 59.768 0 013.27 20.875L5.999 12zm0 0h7.5"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
