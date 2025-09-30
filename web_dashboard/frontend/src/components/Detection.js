import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Camera, AlertCircle, CheckCircle } from 'lucide-react';
import { toast } from 'react-toastify';
import './Detection.css';

const Detection = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [preview, setPreview] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
      
      // Clear previous results
      setDetectionResult(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    maxFiles: 1
  });

  const handleDetection = async () => {
    if (!uploadedFile) {
      toast.error('Please select an image first');
      return;
    }

    setIsDetecting(true);
    
    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);

      const response = await fetch('/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Detection failed');
      }

      const result = await response.json();
      setDetectionResult(result);
      
      toast.success(`Detection completed! Found ${result.total_detections} pests`);
      
    } catch (error) {
      console.error('Detection error:', error);
      toast.error('Detection failed. Please try again.');
    } finally {
      setIsDetecting(false);
    }
  };

  const clearDetection = () => {
    setUploadedFile(null);
    setDetectionResult(null);
    setPreview(null);
  };

  return (
    <div className="detection-page">
      <div className="page-header">
        <h1 className="page-title">Pest Detection</h1>
        <p className="page-subtitle">Upload an image to detect pests using AI</p>
      </div>

      <div className="detection-container">
        {/* Upload Area */}
        <div className="upload-section">
          <div
            {...getRootProps()}
            className={`upload-area ${isDragActive ? 'dragover' : ''}`}
          >
            <input {...getInputProps()} />
            <div className="upload-content">
              <Upload size={48} className="upload-icon" />
              <p className="upload-text">
                {isDragActive
                  ? 'Drop the image here...'
                  : 'Drag & drop an image here, or click to select'
                }
              </p>
              <p className="upload-hint">
                Supports: JPEG, PNG, GIF, BMP, WebP
              </p>
            </div>
          </div>

          {uploadedFile && (
            <div className="file-info">
              <div className="file-details">
                <strong>Selected file:</strong> {uploadedFile.name}
                <br />
                <small>Size: {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</small>
              </div>
              <button className="btn btn-primary" onClick={handleDetection} disabled={isDetecting}>
                {isDetecting ? (
                  <>
                    <div className="spinner"></div>
                    Detecting...
                  </>
                ) : (
                  <>
                    <Camera size={16} />
                    Detect Pests
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Image Preview and Results */}
        {(preview || detectionResult) && (
          <div className="results-section">
            {preview && (
              <div className="image-preview">
                <img src={preview} alt="Upload preview" className="preview-image" />
              </div>
            )}

            {detectionResult && (
              <div className="detection-results">
                <div className="results-header">
                  <h3>Detection Results</h3>
                  <div className="results-summary">
                    <span className="detection-count">
                      {detectionResult.total_detections} pest(s) detected
                    </span>
                    <span className="detection-time">
                      {new Date(detectionResult.timestamp).toLocaleString()}
                    </span>
                  </div>
                </div>

                {detectionResult.detections && detectionResult.detections.length > 0 ? (
                  <div className="detection-list">
                    {detectionResult.detections.map((detection, index) => (
                      <div key={index} className="detection-item">
                        <div className="detection-info">
                          <div className="pest-name">{detection.class_name}</div>
                          <div className="pest-confidence">
                            Confidence: {(detection.confidence * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="confidence-bar">
                          <div
                            className="confidence-fill"
                            style={{
                              width: `${detection.confidence * 100}%`,
                              backgroundColor: detection.confidence > 0.7 ? '#28a745' : 
                                            detection.confidence > 0.4 ? '#ffc107' : '#dc3545'
                            }}
                          ></div>
                        </div>
                        <div className="confidence-text">
                          {(detection.confidence * 100).toFixed(1)}%
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="no-detections">
                    <CheckCircle size={48} />
                    <p>No pests detected in this image</p>
                    <p>Great! Your crop appears to be healthy.</p>
                  </div>
                )}

                <div className="results-actions">
                  <button className="btn btn-success" onClick={() => window.location.reload()}>
                    <Camera size={16} />
                    Detect Another Image
                  </button>
                  <button className="btn btn-secondary" onClick={clearDetection}>
                    Clear Results
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Detection;
