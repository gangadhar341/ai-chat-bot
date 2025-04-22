import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NotFound from "./components/auth/NotFound";
import ErrorBoundary from "./components/auth/ErrorBoundary";
import Chat from "./components/chat/Chat";

function App() {
  return (
    <div className='App'>
      <ErrorBoundary>
        <Router>
          <Routes>
            <Route path='/' element={<Chat />} />
            {/* Wildcard route to catch all undefined paths */}
            <Route path='*' element={<NotFound />} />
          </Routes>
        </Router>
      </ErrorBoundary>
    </div>
  );
}

export default App;
