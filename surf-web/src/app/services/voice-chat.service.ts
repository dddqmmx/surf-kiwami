import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class VoiceChatService {
  private audioContext: AudioContext;
  private audioQueue: { data: Float32Array; duration: number }[] = [];
  private isRecording = false;
  private silentChunks = 0;
  private readonly SILENCE_THRESHOLD = 0.02; // 声音阈值
  private readonly SILENT_CHUNKS = 100; // 连续静音块数量
  private totalRecordedDuration = 0;
  private maxRecordingDuration = 1; // 最大录音时长，单位秒

  constructor() {
    this.audioContext = new AudioContext();
  }

  async initializeRecorder() {
    await this.audioContext.audioWorklet.addModule('/js/audio-processor.js');
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = this.audioContext.createMediaStreamSource(stream);

    // 创建 AudioWorkletNode
    const audioWorkletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');
    source.connect(audioWorkletNode);
    audioWorkletNode.connect(this.audioContext.destination);

    // 监听音频数据
    audioWorkletNode.port.onmessage = (event) => {
      const inputData = event.data as Float32Array;
      this.processAudioInput(inputData);
    };
  }

  private processAudioInput(inputData: Float32Array) {
    const rms = this.computeRMS(inputData);

    if (this.isRecording) {
      this.audioQueue.push({ data: inputData.slice(), duration: inputData.length / this.audioContext.sampleRate });
      this.totalRecordedDuration += inputData.length / this.audioContext.sampleRate;
      if (this.totalRecordedDuration >= this.maxRecordingDuration) {
        this.processAudioSegment();
        this.isRecording = false;
        this.totalRecordedDuration = 0;
      }
      if (rms < this.SILENCE_THRESHOLD) {
        this.silentChunks++;
        if (this.silentChunks > this.SILENT_CHUNKS) {
          this.processAudioSegment();
          this.isRecording = false;
          this.totalRecordedDuration = 0;
        }
      } else {
        this.silentChunks = 0; // 重新计数
      }
    } else if (rms >= this.SILENCE_THRESHOLD) {
      this.isRecording = true;
      this.silentChunks = 0; // 重置静音计数
      this.audioQueue.push({ data: inputData.slice(), duration: inputData.length / this.audioContext.sampleRate });
      this.totalRecordedDuration += inputData.length / this.audioContext.sampleRate;
    }
  }

  private computeRMS(data: Float32Array): number {
    const sum = data.reduce((acc, value) => acc + value * value, 0);
    return Math.sqrt(sum / data.length);
  }

  private processAudioSegment() {
    const audioData = this.combineAudioFrames(this.audioQueue);
    this.audioQueue = []; // 清空队列
    this.playAudio(audioData); // 播放音频数据
  }

  private combineAudioFrames(frames: { data: Float32Array; duration: number }[]): Float32Array {
    const totalLength = frames.reduce((sum, frame) => sum + frame.data.length, 0);
    const combined = new Float32Array(totalLength);
    let offset = 0;

    for (const frame of frames) {
      combined.set(frame.data, offset);
      offset += frame.data.length;
    }
    return combined;
  }

  private playAudio(audioData: Float32Array) {
    const buffer = this.audioContext.createBuffer(1, audioData.length, this.audioContext.sampleRate);
    buffer.copyToChannel(audioData, 0);

    const source = this.audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(this.audioContext.destination);
    source.start();

    source.onended = () => {
      this.isRecording = true; // 恢复录音
      this.totalRecordedDuration = 0;
    };
  }
}
