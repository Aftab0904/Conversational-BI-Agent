import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Send, 
  Bot, 
  User, 
  BarChart2, 
  Table as TableIcon, 
  ChevronRight, 
  Database,
  RefreshCcw,
  Sparkles,
  PieChart as PieChartIcon,
  LineChart as LineChartIcon
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, PieChart, Pie, Cell 
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = "http://localhost:8001/api";

const App = () => {
  const [messages, setMessages] = useState([
    { 
      role: 'ai', 
      content: "Hello! I'm your BI Intelligence Agent. Ask me anything about your data, like 'Top 10 products' or 'Monthly sales trends'.",
      id: Date.now()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(["Top 10 products", "Total orders by department", "Most reordered items"]);
  const scrollRef = useRef(null);

  const scrollToBottom = () => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (queryText = input) => {
    const text = queryText.trim();
    if (!text) return;

    const userMessage = { role: 'user', content: text, id: Date.now() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const lastAIMessage = [...messages].reverse().find(m => m.role === 'ai');
      const response = await axios.post(`${API_BASE}/chat`, {
        query: text,
        last_query: lastAIMessage?.query || ""
      });

      const aiMessage = {
        role: 'ai',
        id: Date.now() + 1,
        ...response.data
      };

      setMessages(prev => [...prev, aiMessage]);
      setSuggestions(response.data.suggestions || []);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: "Error: " + (error.response?.data?.detail || "Mission control communication failure."),
        id: Date.now() + 1,
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <div className="w-72 bg-slate-900/50 border-r border-slate-800 p-6 hidden md:flex flex-col">
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <Database size={24} className="text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">DataMind BI</h1>
        </div>

        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">Saved Collections</div>
          <div className="space-y-2">
            {["Sales Dashboard", "Product Inventory", "Customer Retention"].map(item => (
              <div key={item} className="flex items-center gap-2 p-2 rounded-md hover:bg-slate-800 cursor-pointer transition-colors group">
                <ChevronRight size={14} className="text-slate-600 group-hover:text-indigo-400" />
                <span className="text-sm text-slate-300">{item}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-auto pt-6 border-t border-slate-800">
          <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
            <div className="text-xs font-medium text-slate-400 mb-1">Engine Status</div>
            <div className="flex items-center gap-2 text-sm text-emerald-400">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              Llama 3.3 Active
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Header */}
        <header className="h-16 border-b border-slate-800 flex items-center px-8 bg-slate-950/50 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-indigo-500"></span>
            <span className="text-sm font-medium text-slate-400 italic">Conversational Analytics v2.0</span>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar pb-32">
          {messages.map((m) => (
            <Message key={m.id} message={m} />
          ))}
          {isLoading && (
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center shrink-0">
                <Bot size={18} className="text-white" />
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[80%]">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 left-0 right-0 p-8 bg-gradient-to-t from-slate-950 via-slate-950 to-transparent">
          <div className="max-w-4xl mx-auto space-y-4">
            {/* Suggestions */}
            <div className="flex flex-wrap gap-2 overflow-x-auto no-scrollbar pb-2">
              {suggestions.map((s, i) => (
                <button 
                  key={i}
                  onClick={() => handleSend(s)}
                  className="px-4 py-1.5 bg-slate-900 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-800 text-xs text-slate-300 rounded-full transition-all flex items-center gap-2 shrink-0"
                >
                  <Sparkles size={12} className="text-indigo-400" />
                  {s}
                </button>
              ))}
            </div>

            <div className="relative group">
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask a question about your data..."
                className="w-full bg-slate-900 border border-slate-800 focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 rounded-2xl py-4 px-6 pr-14 text-slate-100 outline-none transition-all shadow-2xl"
              />
              <button 
                onClick={() => handleSend()}
                disabled={isLoading || !input.trim()}
                className="absolute right-3 top-1/2 -translate-y-1/2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-600 text-white p-2.5 rounded-xl transition-all shadow-lg"
              >
                <Send size={18} />
              </button>
            </div>
            <p className="text-[10px] text-center text-slate-600 tracking-wide">
              AI can make mistakes. Verify important results. Powered by Groq Llama 3.3
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const Message = ({ message }) => {
  const isAI = message.role === 'ai';
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-4 ${!isAI ? 'flex-row-reverse' : ''}`}
    >
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-lg ${
        isAI ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 border border-slate-700'
      }`}>
        {isAI ? <Bot size={22} /> : <User size={22} />}
      </div>
      
      <div className={`space-y-4 max-w-[85%] ${!isAI ? 'text-right' : ''}`}>
        <div className={`p-5 rounded-2xl shadow-xl ${
          isAI 
            ? 'bg-slate-900 border border-slate-800 rounded-tl-none text-slate-200' 
            : 'bg-indigo-600 text-white rounded-tr-none'
        }`}>
          {message.content && <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{message.content}</p>}
          {message.summary && <p className="text-[15px] leading-relaxed">{message.summary}</p>}
        </div>

        {isAI && message.data && (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Visualizer Block */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 overflow-hidden">
              <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-4">
                <div className="flex items-center gap-2">
                  <BarChart2 size={18} className="text-indigo-400" />
                  <span className="text-sm font-semibold tracking-wide">Insights Visualization</span>
                </div>
                <div className="flex gap-2">
                  <button className="p-1.5 hover:bg-slate-800 rounded-md transition-colors"><RefreshCcw size={14} className="text-slate-500" /></button>
                </div>
              </div>
              <div className="h-64 w-full">
                <ChartRenderer data={message.data} />
              </div>
            </div>

            {/* Table Block */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
              <div className="bg-slate-800/50 px-6 py-3 border-b border-slate-800 flex items-center gap-2">
                <TableIcon size={16} className="text-slate-400" />
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Data Preview</span>
              </div>
              <div className="overflow-x-auto custom-scrollbar">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-900/50 border-b border-slate-800">
                      {message.columns?.map(col => (
                        <th key={col} className="px-6 py-3 text-[11px] font-bold text-slate-500 uppercase tracking-tighter">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {message.data.slice(0, 5).map((row, i) => (
                      <tr key={i} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                        {message.columns?.map(col => (
                          <td key={col} className="px-6 py-3 text-sm text-slate-300 font-mono">{row[col]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {message.data.length > 5 && (
                <div className="p-3 text-center bg-slate-900/80 border-t border-slate-800">
                  <span className="text-[10px] text-slate-500 font-medium">Showing top 5 of {message.data.length} results</span>
                </div>
              )}
            </div>

            {/* SQL Block */}
            <details className="group">
              <summary className="flex items-center gap-2 cursor-pointer text-[10px] font-bold text-slate-600 uppercase tracking-[0.2em] hover:text-slate-400 transition-colors list-none">
                <div className="w-4 h-4 rounded border border-slate-700 flex items-center justify-center group-open:rotate-90 transition-transform">▶</div>
                Generated SQL Query
              </summary>
              <div className="mt-3 bg-black/40 border border-slate-800 rounded-xl p-4 font-mono text-xs text-indigo-300 overflow-x-auto">
                <pre>{message.sql}</pre>
              </div>
            </details>
          </div>
        )}
      </div>
    </motion.div>
  );
};

const ChartRenderer = ({ data }) => {
  if (!data || data.length === 0) return null;

  // Smart chart selection
  const keys = Object.keys(data[0]);
  const numKeys = keys.filter(k => typeof data[0][k] === 'number');
  const labelKey = keys.find(k => typeof data[0][k] === 'string') || keys[0];
  const valueKey = numKeys[0] || keys[1];

  if (!valueKey) return <div className="h-full flex items-center justify-center text-slate-500 italic text-sm">No numeric data to visualize</div>;

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data.slice(0, 10)}>
        <defs>
          <linearGradient id="colorBar" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
        <XAxis 
          dataKey={labelKey} 
          stroke="#475569" 
          fontSize={10} 
          tickLine={false} 
          axisLine={false}
          tick={{ fill: '#64748b' }}
        />
        <YAxis 
          stroke="#475569" 
          fontSize={10} 
          tickLine={false} 
          axisLine={false}
          tick={{ fill: '#64748b' }}
        />
        <Tooltip 
          contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '12px' }}
          itemStyle={{ color: '#818cf8' }}
        />
        <Bar 
          dataKey={valueKey} 
          fill="url(#colorBar)" 
          stroke="#818cf8" 
          strokeWidth={2}
          radius={[4, 4, 0, 0]} 
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default App;
