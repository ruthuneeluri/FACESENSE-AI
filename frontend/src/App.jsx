import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import History from './pages/History'
import About from './pages/About'

export default function App() {
    return (
        <BrowserRouter>
            <div className="app-container">
                <header className="navbar">
                    <div className="logo">FaceSense AI</div>
                    <nav>
                        <a href="/">Home</a>
                        <a href="/analyze">Analyze</a>
                        <a href="/history">History</a>
                        <a href="/about">About</a>
                    </nav>
                </header>
                <main>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/analyze" element={<Analyze />} />
                        <Route path="/history" element={<History />} />
                        <Route path="/about" element={<About />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    )
}
