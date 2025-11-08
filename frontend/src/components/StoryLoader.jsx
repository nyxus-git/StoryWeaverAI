import { useState, useEffect } from 'react';
import { useParams, useNavigate } from "react-router-dom"
import axios from 'axios';
import LoadingStatus from "./LodingStatus.jsx"
import StoryGame from './StoryGame.jsx';

// --- FIX 1: Use the full backend server address ---
// (This assumes your util.js file has the correct http://127.0.0.1:8000 URL)
// If you don't have util.js, define it here:
const API_BASE_URL = "http://127.0.0.1:8000/api";

function StoryLoader() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [story, setStory] = useState(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null);

    // --- FIX 2: Call loadStory inside a useEffect ---
    // This runs the function when the component loads
    useEffect(() => {
        if (id) {
            loadStory(id);
        }
    }, [id]); // The [id] means it will re-run if the story ID in the URL changes

    const loadStory = async (storyId) => {
        setLoading(true)
        setError(null)

        try {
            // --- FIX 3: Use backticks (`) instead of single quotes (') ---
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
            
            setStory(response.data);
            
            // --- FIX 4: Removed the typo 'setLoading(response.false)' ---
            
        } catch (err) {
            if (err.response?.status === 404) {
                setError("Story is not found");
            } else {
                setError("Failed To Load Story");
            }
        } finally {
            setLoading(false);
        }
    }

    const createNewStory = async () => {
        navigate("/");
    }

    if (loading) {
        return <LoadingStatus theme={'story'} />;
    }

    if (error) {
        return <div className="error-container">
            <div className='error-message'>
                {/* Updated this to show the specific error */}
                <h2>{error}</h2>
                <p>The story you are looking for could not be loaded.</p>
                <button onClick={createNewStory}> Go to Story Generator </button>
            </div>
        </div>
    }

    if (story) {
        return <div className="story-loader">
            <StoryGame story={story} onNewStory={createNewStory} />
        </div>
    }

    // Added a default return
    return null;
}

export default StoryLoader;