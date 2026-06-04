"use client";

import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { ArrowLeft, Loader2, AlertTriangle, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

interface ForecastData {
  week: string;
  predicted_occupancy: number;
  adr?: number;
  revpar?: number;
  events?: string[];
}

export default function Dashboard() {
  const [data, setData] = useState<ForecastData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [threshold, setThreshold] = useState(0.65);
  const [marketing, setMarketing] = useState<any>(null);
  const [loadingMarketing, setLoadingMarketing] = useState(false);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    fetch(`${apiUrl}/api/forecast`)
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch forecast. Has the pipeline run?");
        return res.json();
      })
      .then(json => {
        setData(json.forecast);
        setThreshold(json.alert_threshold);
        setLoading(false);
        
        // Check if any week dips below threshold
        const dip = json.forecast.find((d: any) => d.predicted_occupancy < json.alert_threshold);
        if (dip) {
          fetchMarketing(dip.predicted_occupancy);
        }
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const fetchMarketing = async (occupancy: number) => {
    setLoadingMarketing(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      const res = await fetch(`${apiUrl}/api/marketing?occupancy=${occupancy}`);
      const json = await res.json();
      setMarketing(json);
    } catch (e) {
      console.error(e);
    }
    setLoadingMarketing(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center text-[#ebff00]">
        <Loader2 className="w-12 h-12 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center text-red-500 font-mono">
        <div className="bg-red-950 p-8 border border-red-500">
          <AlertTriangle className="w-12 h-12 mb-4" />
          <h1 className="text-xl font-bold">SYSTEM ERROR</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white font-mono p-8">
      <Link href="/" className="inline-flex items-center text-[#ebff00] hover:underline mb-8">
        <ArrowLeft className="w-4 h-4 mr-2" />
        RETURN TO SYSTEM BOOT
      </Link>

      <header className="mb-12 border-b border-[#ebff00] pb-4">
        <h1 className="text-4xl font-black text-[#ebff00] uppercase">Demand Forecast Dashboard</h1>
        <p className="text-gray-400 mt-2">Next 12 Weeks ML Prediction Pipeline</p>
        
        <div className="mt-6 bg-[#111] p-4 border-l-4 border-[#ebff00] text-sm text-gray-300 max-w-4xl">
          <strong className="text-white block mb-1">How it Works:</strong>
          The XGBoost pipeline predicts future occupancy based on historical pacing and local events. 
          When the yellow forecast line dips below the red safety threshold (65%), it represents a dangerous drop in expected revenue. 
          The moment this drop is detected, the Minimax AI Agent automatically activates to generate targeted marketing campaigns to plug the gap before it happens!
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 flex flex-col gap-8">
          <div className="bg-[#111] p-6 border border-gray-800">
            <h2 className="text-xl font-bold mb-6 flex justify-between">
              <span>Occupancy Forecast</span>
              <span className="text-sm font-normal text-gray-500">Threshold: {(threshold * 100).toFixed(0)}%</span>
            </h2>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="week" stroke="#888" tick={{ fill: '#888' }} />
                  <YAxis stroke="#888" tick={{ fill: '#888' }} domain={[0, 1]} tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #ebff00', color: '#ebff00' }}
                    itemStyle={{ color: '#ebff00' }}
                    formatter={(value: any) => [`${(Number(value) * 100).toFixed(1)}%`, 'Occupancy']}
                  />
                  {/* Threshold line */}
                  <Line type="monotone" dataKey={() => threshold} stroke="#ef4444" strokeWidth={2} strokeDasharray="5 5" dot={false} name="Threshold" />
                  {/* Forecast line */}
                  <Line type="monotone" dataKey="predicted_occupancy" stroke="#ebff00" strokeWidth={3} dot={{ fill: '#0a0a0a', stroke: '#ebff00', strokeWidth: 2 }} activeDot={{ r: 8 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-[#111] p-6 border border-gray-800">
            <h2 className="text-xl font-bold mb-6 text-[#ebff00]">RevPAR Forecast (Revenue per Room)</h2>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="week" stroke="#888" tick={{ fill: '#888' }} />
                  <YAxis stroke="#888" tick={{ fill: '#888' }} tickFormatter={(val) => `$${val}`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #ebff00', color: '#ebff00' }}
                    itemStyle={{ color: '#ebff00' }}
                    formatter={(value: any) => [`$${value}`, 'RevPAR']}
                  />
                  <Line type="monotone" dataKey="revpar" stroke="#ebff00" strokeWidth={3} dot={{ fill: '#0a0a0a', stroke: '#ebff00', strokeWidth: 2 }} activeDot={{ r: 8 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-8">
          <div className="bg-[#111] p-6 border border-gray-800">
          <h2 className="text-xl font-bold mb-6 text-[#ebff00] border-b border-[#ebff00] pb-2">AI Marketing Agent</h2>
          
            {loadingMarketing ? (
              <div className="flex flex-col items-center justify-center py-12 text-gray-400">
                <Loader2 className="w-8 h-8 animate-spin text-[#ebff00] mb-4" />
                <p>Minimax M3 generating strategy...</p>
              </div>
            ) : marketing ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                {marketing.error ? (
                  <div className="text-red-500 bg-red-950 p-4 border border-red-500">
                    <AlertTriangle className="inline w-5 h-5 mr-2" />
                    {marketing.error}
                  </div>
                ) : (
                  <>
                    <div className="bg-[#0a0a0a] p-4 border border-[#ebff00]">
                      <h3 className="font-bold text-[#ebff00] mb-2 uppercase">Subject Line</h3>
                      <p className="text-lg">{marketing.email_subject}</p>
                    </div>
                    <div className="bg-[#0a0a0a] p-4 border border-[#ebff00]">
                      <h3 className="font-bold text-[#ebff00] mb-2 uppercase">WhatsApp Copy</h3>
                      <p className="text-sm">{marketing.whatsapp_message}</p>
                    </div>
                    <div className="bg-[#0a0a0a] p-4 border border-[#ebff00]">
                      <h3 className="font-bold text-[#ebff00] mb-2 uppercase">Instagram</h3>
                      <p className="text-sm">{marketing.instagram_caption}</p>
                    </div>
                    <div className="bg-[#0a0a0a] p-4 border border-gray-800">
                      <h3 className="font-bold text-gray-400 mb-2 uppercase">Target Audience</h3>
                      <p className="text-sm text-gray-300">{marketing.target_segment}</p>
                    </div>
                    <div className="bg-[#0a0a0a] p-4 border border-gray-800">
                      <h3 className="font-bold text-gray-400 mb-2 uppercase">Suggested Discount</h3>
                      <p className="text-lg font-black text-[#ebff00]">{marketing.recommended_discount}</p>
                    </div>
                  </>
                )}
              </motion.div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-gray-500 text-center">
                <CheckCircle2 className="w-12 h-12 mb-4 text-green-500" />
                <p>Forecast is healthy.<br/>No marketing intervention required.</p>
              </div>
            )}
          </div>

          <div className="bg-[#111] p-6 border border-gray-800">
            <h2 className="text-xl font-bold mb-6 text-white border-b border-gray-800 pb-2">Upcoming Events</h2>
            <div className="space-y-4">
              {data.filter(d => d.events && d.events.length > 0).length === 0 ? (
                <p className="text-gray-500 text-sm">No major events found in the forecast period.</p>
              ) : (
                data.filter(d => d.events && d.events.length > 0).map((d, i) => (
                  <div key={i} className="flex flex-col bg-[#0a0a0a] p-3 border border-gray-800">
                    <span className="text-xs text-[#ebff00] font-bold">{d.week}</span>
                    <ul className="list-disc list-inside text-gray-300 mt-1">
                      {d.events!.map((e, j) => (
                        <li key={j} className="text-sm">{e}</li>
                      ))}
                    </ul>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
