#!/usr/bin/env python3
"""JARVIS v12.1.2 — Production Cognitive Platform."""
from __future__ import annotations
import argparse, json, os, sys, threading, time, logging
from pathlib import Path

# --- Logging setup first ---
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger=logging.getLogger("jarvis")

# --- Graceful import wrapper ---
_IMPORT_ERRORS={}

def _safe_import(module_path, default=None):
    try:
        parts=module_path.split('.'); module=__import__(module_path,fromlist=[parts[-1]])
        return getattr(module,parts[-1],module) if len(parts)==1 else module
    except Exception as e:
        _IMPORT_ERRORS[module_path]=str(e); logger.debug(f"Optional import failed: {module_path} ({e})")
        return default

def _safe_import_from(module,name,default=None):
    try: mod=__import__(module,fromlist=[name]); return getattr(mod,name)
    except Exception as e:
        _IMPORT_ERRORS[f"{module}.{name}"]=str(e); logger.debug(f"Optional import failed: {module}.{name} ({e})")
        return default

# --- Core imports ---
from core import ModelRouter, ToolRegistry, SecurityGuard, EventBus
from core.checkpoint import CheckpointManager
from core.watchdog import Watchdog
from core.hardware_profiler import HardwareProfiler
from core.persona import PERSONAS, PersonaManager
from core.tool_cache import ToolCache
from core.self_healing import SelfHealingRetry
from core.react_engine import ReActEngine
from core.native_model_loader import NativeModelLoader
from core.native_backend import NativeInferenceBackend
from core.openai_compatible_backend import OpenAICompatibleBackend
from core.model_swarm import ModelSwarm
from core.orchestrator import Orchestrator
from core.predictor import InputPredictor
from core.auto_programmer import AutoProgrammer
from core.sandbox_validator import SandboxValidator
from core.lora_manager import LoRAManager
from core.distributed_backend import DistributedBackend
from core.network_coordinator import NetworkCoordinator
from core.model_registry import ModelRegistry
from core.strategy_engine import StrategyEngine
from core.verification import VerificationEngine
from core.cognitive_state import CognitiveStateMachine
from core.resource_manager import ResourceManager
from core.gpu_scheduler import GPUScheduler
from core.model_discovery import ModelDiscovery
from core.learned_router import LearnedRouter
from core.failure_memory import FailureMemory
from core.mission_engine import MissionEngine
from core.workflow_engine import WorkflowEngine, WorkflowResult
from core.hybrid_retrieval import HybridRetriever
from core.plugin_policy import PluginPolicy
from core.model_capability_graph import ModelCapabilityGraph
from core.execution_policy import ExecutionPolicy
from core.audit import AuditLog
from core.permission_engine import PermissionEngine
from core.doctor import Doctor
from core.model_benchmark import ModelBenchmark
from core.knowledge_graph import KnowledgeGraph
from core.aion_planner import AIONPlanner
from core.learning_pipeline import LearningPipeline
from core.security_executor import SecurityExecutor
from core.self_edit_guard import SelfEditGuard
from core.continual_learning import ContinualLearningLab
from core.model_benchmark_lab import ModelBenchmarkLab
from core.multi_gpu_runtime import MultiGPURuntime
from core.rag_engine import RAGEngine
from core.aion3 import AION3
from aion_bridge.cognitive_engine import AION
from aion_bridge.bridge import AIONBridge
from core.continual_lab import ContinualLab
from core.cognitive_platform import CognitivePlatform
from core.hardware_certification import HardwareCertification

# --- Optional subsystems ---
UnifiedMemory=_safe_import_from("memory","UnifiedMemory")
EmbeddingEngine=_safe_import_from("memory","EmbeddingEngine")
ConsolidationEngine=_safe_import_from("memory","ConsolidationEngine")
DocumentIngestor=_safe_import_from("knowledge.document_ingestor","DocumentIngestor")
SelfAwareness=_safe_import_from("knowledge.self_awareness","SelfAwareness")
AgentManager=_safe_import_from("agents","AgentManager")
NLScheduler=_safe_import_from("agents.scheduler","NLScheduler")
STTEngine=_safe_import_from("voice","STTEngine")
WakeWordDetector=_safe_import_from("voice.wake_word","WakeWordDetector")
ConversationLoop=_safe_import_from("voice.conversation_loop","ConversationLoop")
VoiceState=_safe_import_from("voice.conversation_loop","VoiceState")
StructuredLogger=_safe_import_from("observability","StructuredLogger")
fastapi_app=_safe_import_from("api.server","app")

# --- Tools ---
calculator_tool=_safe_import_from("tools","calculator_tool")
file_tools=_safe_import_from("tools","file_tools")
shell_tool=_safe_import_from("tools","shell_tool")
web_search_tool=_safe_import_from("tools","web_search_tool")
code_executor_tool=_safe_import_from("tools","code_executor_tool")
BrowserAutomation=_safe_import_from("tools.browser_automation","BrowserAutomation")
self_edit=_safe_import_from("tools.self_edit","self_edit")
voice_tools=_safe_import_from("voice","voice_tools")
computer_use_tools=_safe_import_from("computer.computer_use","computer_use_tools")

PROJECT_ROOT=Path(__file__).resolve().parent

def _anchor_config_paths(cfg: dict, root: Path) -> dict:
    """Anchor writable runtime state under Flet app storage when packaged."""
    runtime_root=Path(os.environ.get("FLET_APP_STORAGE_DATA", str(root / "data"))).resolve(); runtime_root.mkdir(parents=True,exist_ok=True)
    def runtime_path(value):
        if not value:return value
        p=Path(str(value)).expanduser()
        if p.is_absolute():return str(p)
        parts=list(p.parts)
        if parts and parts[0].lower()=="data":parts=parts[1:]
        return str((runtime_root.joinpath(*parts)).resolve())
    native=cfg.setdefault("native",{}); native["model_dirs"]=[str(Path(v).expanduser().resolve()) for v in native.get("model_dirs",[]) if isinstance(v,str)]
    memory=cfg.setdefault("memory",{})
    if memory.get("lance_path"):memory["lance_path"]=runtime_path(memory["lance_path"])
    if memory.get("db_path"):memory["db_path"]=runtime_path(memory["db_path"])
    security=cfg.setdefault("security",{})
    for key in ("workspace_root","audit_log"):
        if security.get(key):security[key]=runtime_path(security[key])
    obs=cfg.setdefault("observability",{})
    if obs.get("log_path"):obs["log_path"]=runtime_path(obs["log_path"])
    bridge=cfg.setdefault("aion_bridge",{})
    if bridge.get("journal_path"):bridge["journal_path"]=runtime_path(bridge["journal_path"])
    return cfg


def load_config(path: str|None=None) -> dict:
    config_path=Path(path) if path else (PROJECT_ROOT/"config.json")
    if not config_path.is_absolute() and not config_path.exists(): config_path=PROJECT_ROOT/config_path
    with open(config_path,encoding="utf-8") as f: cfg=json.load(f)
    cfg = _anchor_config_paths(cfg, config_path.resolve().parent)
    from core.strict_config import validate_security_dict
    validate_security_dict(cfg.get("security",{}))
    return cfg

class _FallbackLogger:
    def info(self,e,d=None): logger.info(f"{e}: {d}")
    def warn(self,e,d=None): logger.warning(f"{e}: {d}")
    def error(self,e,d=None): logger.error(f"{e}: {d}")
    def critical(self,e,d=None): logger.critical(f"{e}: {d}")

class JARVISCore:
    VERSION="12.1.2"

    def __init__(self, cfg: dict):
        self.cfg=cfg; self.version=self.VERSION; self._shutdown=False; self._threads: list[threading.Thread]=[]; self.current_session="default"
        self.logger=StructuredLogger(log_path=cfg.get("observability",{}).get("log_path","data/jarvis.jsonl"),
            max_mb=cfg.get("observability",{}).get("max_log_mb",10),
            retain_days=cfg.get("observability",{}).get("retain_days",7)) if StructuredLogger else _FallbackLogger()
        self.logger.info("jarvis_startup",{"version":self.version,"import_errors":len(_IMPORT_ERRORS)})
        self.audit=AuditLog(cfg.get("security",{}).get("audit_log","data/audit.jsonl"))
        self.event_bus=EventBus()
        self.guard=SecurityGuard(workspace_root=cfg.get("security",{}).get("workspace_root","data/workspace"),
                                 allow_shell=cfg.get("security",{}).get("allow_shell",False))
        self.profiler=HardwareProfiler()
        self.loader=NativeModelLoader(cfg.get("native",{}).get("model_dirs",["~/models"]),
                                      cfg.get("native",{}).get("extensions",[".gguf"]))
        discovered=self.loader.discover()
        self.logger.info("models_discovered",{"count":len(discovered),"models":[m.name for m in discovered]})
        self.swarm=ModelSwarm(max_vram_gb=self.profiler.vram_free_gb)
        for m in discovered: self.swarm.register(m)
        self.orchestrator=None
        self.predictor=InputPredictor()
        self._preload_thread=None
        self.router=ModelRouter(cfg)
        self.router.set_swarm(self.swarm, cfg.get("native",{}))
        for m in discovered:
            backend=NativeInferenceBackend(m.path,cfg.get("native",{}),m)
            self.router.register_backend(m.name,backend,m)
        if discovered:
            best=self.swarm.select_best(self.profiler.vram_free_gb,"general")
            if best: self.router.set_primary(best.name); self.logger.info("auto_selected_model",{"model":best.name})
        self._register_external_backends(cfg)
        self.orchestrator=Orchestrator(self.swarm, router=self.router)
        mem_cfg=cfg.get("memory",{})
        self.memory=UnifiedMemory(db_path=mem_cfg.get("db_path"),lance_uri=mem_cfg.get("lance_path","data/jarvis_lance"),max_history=mem_cfg.get("max_history",100),max_sessions=mem_cfg.get("max_sessions",1000)) if UnifiedMemory else None
        self.retriever=HybridRetriever(getattr(self.memory,"store",None)) if self.memory else None
        self.aion=AION(store=getattr(self.memory,"lance",None)) if self.memory else None
        self.model_registry=ModelRegistry(store=getattr(self.memory,"lance",None)) if self.memory else None
        for m in discovered:
            if self.model_registry:self.model_registry.register(m, tags=list(getattr(m,"capabilities",[])))
        self.strategy_engine=StrategyEngine()
        self.verifier=VerificationEngine()
        self.cognitive=CognitiveStateMachine()
        self.resources=ResourceManager()
        self.gpu_scheduler=GPUScheduler(self.resources)
        self.model_benchmark=ModelBenchmark(self.model_registry,self.gpu_scheduler) if self.model_registry else None
        self.model_discovery=ModelDiscovery(cfg.get("native",{}).get("model_dirs",["~/models"]))
        self.capability_graph=ModelCapabilityGraph()
        scfg=cfg.get("security",{})
        self.execution_policy=ExecutionPolicy(allow_network=scfg.get("allow_network",False),
            allow_shell=scfg.get("allow_shell",False),require_approval_for_high_risk=scfg.get("require_approval_for_high_risk",True),
            mode=scfg.get("mode","guarded"),allowed_capabilities=scfg.get("allowed_capabilities",[]),audit=self.audit)
        for discovered_model in self.model_discovery.scan(): self.capability_graph.add_model(discovered_model)
        self.learned_router=LearnedRouter(self.model_registry) if self.model_registry else None
        if self.learned_router:
            for m in discovered:
                self.learned_router.register_features(m.name, list(getattr(m,"capabilities",[])))
            self.router.set_learned_router(self.learned_router)
        self.failure_memory=FailureMemory()
        self.knowledge_graph=KnowledgeGraph(getattr(self.memory,"lance",None)) if self.memory else None
        self.aion_planner=AIONPlanner()
        self.learning_pipeline=LearningPipeline()
        self.missions=MissionEngine(store=getattr(self.memory,"lance",None))
        self.workflows=WorkflowEngine(store=getattr(self.memory,"lance",None))
        self.plugin_policy=PluginPolicy(cfg.get("plugins",{}).get("allowed_capabilities",[]))
        self.learning_lab=ContinualLearningLab()
        self.benchmark_lab=ModelBenchmarkLab(self.profiler,self.model_registry) if self.model_registry else None
        self.multi_gpu=MultiGPURuntime(self.gpu_scheduler)
        self.rag3=RAGEngine(self.retriever,self.knowledge_graph) if self.retriever else None
        self.aion3=AION3(self.aion_planner, store=getattr(self.memory,"lance",None))
        self.aion_bridge=AIONBridge(store=getattr(self.memory,"lance",None), poll_interval=float(cfg.get("aion_bridge",{}).get("poll_interval",2)))
        if cfg.get("aion_bridge",{}).get("enabled",False):
            try:self.aion_bridge.connect()
            except Exception as exc:self.logger.warn("aion_bridge_start_failed",{"error":str(exc)})
        self.continual_lab=ContinualLab()
        self.hardware_cert=HardwareCertification()
        self.embedder=EmbeddingEngine() if EmbeddingEngine else None
        self.consolidator=ConsolidationEngine(self.memory,self.router) if ConsolidationEngine and self.memory else None
        self.security_executor=SecurityExecutor(self.execution_policy,self.audit)
        self.registry=ToolRegistry(authorizer=self.execution_policy.engine,audit=self.audit)
        self._register_tools()
        from protocols.mcp_protocol import MCPServer
        self.mcp=MCPServer(self.registry)
        self.tool_cache=ToolCache(ttl_seconds=cfg.get("tool_cache",{}).get("ttl",300))
        self.router.tool_cache=self.tool_cache
        self.healer=SelfHealingRetry(self.registry)
        self.react=ReActEngine(self.router,self.registry,max_steps=int(cfg.get('react',{}).get('max_steps',5)))
        self.sandbox=SandboxValidator()
        self.auto_programmer=AutoProgrammer(self.registry,self.sandbox,generator=lambda prompt:self.router.chat(prompt))
        self.self_edit_guard=SelfEditGuard(PROJECT_ROOT,allow_apply=cfg.get("self_edit",{}).get("allow_apply",False))
        self.self_aware=SelfAwareness(project_root=str(PROJECT_ROOT),memory=self.memory) if SelfAwareness else None
        if cfg.get("self_awareness",{}).get("enabled",False) and self.self_aware:
            self._start_background_self_awareness()
        self.lora=LoRAManager()
        self.scheduler=NLScheduler(self.memory) if self.memory else None
        self.task_manager=AgentManager() if AgentManager else None
        self._register_default_agents()
        self.checkpoint=CheckpointManager()
        self.stt=STTEngine() if STTEngine else None
        self.wake=WakeWordDetector(phrases=cfg.get("voice",{}).get("wake_phrases",["hey jarvis","jarvis"])) if WakeWordDetector else None
        self.voice_loop=None
        if ConversationLoop and self.stt and self.wake and voice_tools:
            try: self.voice_loop=ConversationLoop(self.stt,self._chat_sync,voice_tools()[0],self.wake)
            except Exception as e: logger.warning(f"Voice loop init failed: {e}")
        self.distributed=None
        if cfg.get("distributed",{}).get("enabled",False):
            try:
                coord=NetworkCoordinator(port=cfg["distributed"].get("coordinator_port",28766),
                    auth_token=cfg["distributed"].get("auth_token",""))
                self.distributed=DistributedBackend(coordinator=coord)
            except Exception as e: logger.warning(f"Distributed init failed: {e}")
        self.persona="default"
        self.watchdog=Watchdog(check_interval=float(cfg.get("watchdog",{}).get("check_interval",5)),max_restarts=int(cfg.get("watchdog",{}).get("max_restart_attempts",3)))
        self.watchdog.add_check("router",lambda: bool(self.router.backends) or self._shutdown)
        self.watchdog.add_check("memory",lambda: bool(self.memory and (self.memory.lance or self.memory.sqlite)) or self._shutdown)
        if cfg.get("watchdog",{}).get("enabled",True):self.watchdog.start()
        # Optional Qwen/Ollama provider joins the same unified model plane.
        if cfg.get("qwen",{}).get("enabled",False):
            try:
                from qwen_integration.backend import QwenBackend
                qb=QwenBackend(cfg["qwen"].get("api_base"),cfg["qwen"].get("default_model","qwen3:8b"))
                self.router.register_backend("qwen",qb,qb.spec)
            except Exception as exc:self.logger.warn("qwen_backend_registration_failed",{"error":str(exc)})
        if cfg.get("scheduler",{}).get("enabled",False): self._start_scheduler_worker()
        self._start_proactive_monitoring()
        self._start_nightly_consolidation()
        if cfg.get("lora",{}).get("nightly_train",False): self._start_nightly_lora()
        self.logger.info("jarvis_ready",{"persona":self.persona,"models":len(discovered)})

    def _register_external_backends(self, cfg: dict):
        """Register optional OpenAI-compatible local servers without coupling JARVIS to them."""
        for item in cfg.get("external_backends", []):
            if not item.get("enabled", False):
                continue
            try:
                name = str(item.get("name") or "external")
                spec = __import__("core.types", fromlist=["ModelSpec"]).ModelSpec(
                    name=str(item.get("model") or name), backend="openai_compatible",
                    capabilities=list(item.get("capabilities", ["general"])))
                api_key = os.environ.get(str(item.get("api_key_env", ""))) if item.get("api_key_env") else item.get("api_key")
                backend = OpenAICompatibleBackend(
                    spec, str(item.get("base_url", "http://127.0.0.1:8080/v1")),
                    api_key=api_key, timeout=int(item.get("timeout", 120)), model=item.get("model"))
                self.router.register_backend(name, backend, spec)
                if item.get("primary", False):
                    self.router.set_primary(name)
            except Exception as exc:
                self.logger.warn("external_backend_registration_failed", {"error": str(exc)})

    def _start_background_self_awareness(self):
        def scan():
            try:
                self.self_aware.scan()
                self.logger.info("self_awareness_scan_complete", self.self_aware.get_stats())
            except Exception as exc:
                self.logger.warn("self_awareness_scan_failed", {"error": str(exc)})
        t = threading.Thread(target=scan, name="jarvis-self-awareness", daemon=True)
        t.start(); self._threads.append(t)

    def _register_default_agents(self):
        if not self.task_manager: return
        templates=[("coder",["code","debug","refactor"]),("research",["web","research","summarize"]),("system",["process","system","automation"]),("file",["filesystem.read","filesystem.write","file"]) ]
        for name,caps in templates:
            if not any(a.name==name for a in self.task_manager.agents.values()):
                self.task_manager.register(name,caps)

    def ingest_document(self, file_path: str) -> dict:
        if not DocumentIngestor or not self.memory: raise RuntimeError("Document ingestion is unavailable")
        p=Path(file_path).resolve()
        if not p.is_file(): raise FileNotFoundError(str(p))
        workspace=self.guard.workspace.resolve()
        if workspace not in p.parents and p != workspace: raise PermissionError("document is outside workspace")
        ingestor=DocumentIngestor()
        chunks=list(ingestor.ingest(str(p))); embedded=0
        for chunk in chunks:
            vector=self.embedder.embed(chunk["text"]) if self.embedder else None
            self.memory.add_document(chunk["id"],chunk["text"],chunk["metadata"],vector=vector)
            self.retriever.index(chunk["id"],chunk["text"])
            embedded += int(vector is not None)
        return {"file":str(p),"chunks":len(chunks),"embedded":embedded,"vector_search":embedded>0}

    def _register_tools(self):
        from core.types import ToolSpec, RiskLevel
        def schema(props, required=()): return {"type":"object","properties":props,"required":list(required),"additionalProperties":False}
        self.registry.register(ToolSpec("calculator","Safe arithmetic calculator",schema({"expression":{"type":"string","minLength":1,"maxLength":4096}},("expression",)),calculator_tool,[],RiskLevel.LOW))
        if file_tools:
            ft=file_tools()
            workspace=str(self.guard.workspace)
            self.registry.register(ToolSpec("file_read","Read a workspace file",schema({"path":{"type":"string","maxLength":1024}},("path",)),lambda path: ft["read"](path,workspace),["filesystem.read"],RiskLevel.LOW))
            self.registry.register(ToolSpec("file_write","Write a workspace file",schema({"path":{"type":"string","maxLength":1024},"content":{"type":"string","maxLength":2_000_000}},("path","content")),lambda path,content: ft["write"](path,content,workspace),["filesystem.write"],RiskLevel.HIGH))
        if shell_tool:
            def secure_shell(command,timeout=30,cwd=None,_authorization_granted=False): return self.security_executor.run(__import__('shlex').split(command),cwd=cwd,timeout=timeout,_authorization_granted=_authorization_granted)
            self.registry.register(ToolSpec("shell","Sandboxed argv command execution",schema({"command":{"type":"string","minLength":1,"maxLength":8192},"timeout":{"type":"integer","minimum":1,"maximum":600},"cwd":{"type":"string","maxLength":1024}},("command",)),secure_shell,["process"],RiskLevel.HIGH))
        if web_search_tool: self.registry.register(ToolSpec("web_search","Web search",schema({"query":{"type":"string","minLength":1,"maxLength":8192},"max_results":{"type":"integer","minimum":1,"maximum":20}},("query",)),web_search_tool,["web"],RiskLevel.LOW))
        if code_executor_tool:
            def secure_code(code,language="python",timeout=30,_authorization_granted=False): return code_executor_tool(code,language,timeout)
            self.registry.register(ToolSpec("code_exec","Sandboxed Python execution",schema({"code":{"type":"string","minLength":1,"maxLength":1_000_000},"language":{"type":"string","enum":["python"]},"timeout":{"type":"integer","minimum":1,"maximum":600}},("code",)),secure_code,["code"],RiskLevel.HIGH))
        if BrowserAutomation: self.registry.register(ToolSpec("browser","Validated browser navigation",schema({"url":{"type":"string","minLength":1,"maxLength":4096}},("url",)),BrowserAutomation().navigate,["browser"],RiskLevel.HIGH))
        if computer_use_tools:
            for tool_name, handler in computer_use_tools().items():
                risk=RiskLevel.HIGH if tool_name in {"click","type_text"} else RiskLevel.MEDIUM if hasattr(RiskLevel,"MEDIUM") else RiskLevel.HIGH
                props={}
                required=[]
                if tool_name=="click": props={"x":{"type":"integer"},"y":{"type":"integer"},"button":{"type":"string","enum":["left","right","middle"]}}; required=["x","y"]
                elif tool_name=="type_text": props={"text":{"type":"string","maxLength":10000},"interval":{"type":"number","minimum":0,"maximum":1}}; required=["text"]
                elif tool_name=="get_cursor_pos": props={}; required=[]
                else: props={}; required=[]
                self.registry.register(ToolSpec("computer_"+tool_name,"Computer control: "+tool_name,schema(props,required),handler,["computer"],risk))
        if self_edit:
            def guarded_self_edit(file_path,old_code,new_code,dry_run=True,_authorization_granted=False):
                target=(PROJECT_ROOT/Path(file_path)).resolve()
                if not target.is_relative_to(PROJECT_ROOT) or not target.is_file(): return {"ok":False,"error":"invalid self-edit target"}
                current=target.read_text(encoding="utf-8")
                if current!=old_code and old_code not in current: return {"ok":False,"error":"old_code not found"}
                replacement=current.replace(old_code,new_code,1)
                prepared=self.self_edit_guard.prepare(target.relative_to(PROJECT_ROOT),replacement)
                if dry_run: return prepared
                return self.self_edit_guard.apply(prepared,authorization_granted=_authorization_granted)
            self.registry.register(ToolSpec("self_edit","Transactional self-modification",schema({"file_path":{"type":"string","maxLength":1024},"old_code":{"type":"string","maxLength":1_000_000},"new_code":{"type":"string","maxLength":1_000_000},"dry_run":{"type":"boolean"}},("file_path","old_code","new_code")),guarded_self_edit,["meta"],RiskLevel.HIGH))

    def _start_scheduler_worker(self):
        if not self.scheduler: return
        def loop():
            interval=max(0.25,float(self.cfg.get("scheduler",{}).get("poll_interval",1.0)))
            while not self._shutdown:
                task=self.scheduler.next_task()
                if task:
                    try:
                        result=self.chat(task.description,session_id=f"scheduled:{task.task_id}")
                        self.scheduler.complete_task(task.task_id)
                        self.logger.info("scheduled_task_completed",{"task_id":task.task_id,"result_length":len(result)})
                    except Exception as exc:
                        task.status="failed"
                        self.logger.warn("scheduled_task_failed",{"task_id":task.task_id,"error":str(exc)})
                else:
                    time.sleep(interval)
        t=threading.Thread(target=loop,name="jarvis-scheduler",daemon=True); t.start(); self._threads.append(t)

    def _start_proactive_monitoring(self):
        pcfg=self.cfg.get("proactive",{})
        if not pcfg.get("enabled",True): return
        def loop():
            while not self._shutdown:
                try:
                    import psutil
                    disk=psutil.disk_usage(str(Path.home().anchor or os.path.abspath(os.sep))).percent; cpu=psutil.cpu_percent(interval=1); mem=psutil.virtual_memory().percent
                    if disk>pcfg.get("disk_threshold",90): self.logger.warn("proactive_disk_warning",{"percent":disk})
                    if cpu>pcfg.get("cpu_threshold",95): self.logger.warn("proactive_cpu_warning",{"percent":cpu})
                    if mem>pcfg.get("memory_threshold",90): self.logger.warn("proactive_memory_warning",{"percent":mem})
                except Exception as exc: self.logger.warn("proactive_monitor_failed", {"error": str(exc)})
                time.sleep(60)
        t=threading.Thread(target=loop,daemon=True); t.start(); self._threads.append(t)

    def _start_nightly_consolidation(self):
        if not self.cfg.get("consolidation",{}).get("nightly_enabled",True): return
        def loop():
            while not self._shutdown:
                now=time.localtime()
                if now.tm_hour==3 and self.consolidator:
                    try: self.consolidator.run()
                    except Exception as e: logger.error(f"Consolidation error: {e}")
                    time.sleep(3600)
                time.sleep(300)
        t=threading.Thread(target=loop,daemon=True); t.start(); self._threads.append(t)

    def _start_nightly_lora(self):
        def loop():
            while not self._shutdown:
                now=time.localtime()
                if now.tm_hour==4:
                    primary=self.router.primary
                    if primary and hasattr(primary,"model_path"):
                        try:
                            from training.lora_trainer import LoRATrainer
                            trainer=LoRATrainer(); result=trainer.run_nightly(primary.model_path)
                            self.logger.info("lora_nightly",result)
                        except Exception as e: logger.error(f"LoRA nightly error: {e}")
                    time.sleep(3600)
                time.sleep(300)
        t=threading.Thread(target=loop,daemon=True); t.start(); self._threads.append(t)

    def _chat_sync(self, message: str, stream: bool=False) -> str: return self.chat(message,stream=stream)

    def chat(self, message: str, stream: bool=False, task_type: str="default", session_id: str="default") -> str:
        self.swarm.update_capacity(self.profiler.vram_free_gb)
        self.cognitive.transition("perceive","new user request")
        history=self.memory.get_history(session_id=session_id,limit=self.cfg.get("memory",{}).get("max_history",100)) if self.memory else []
        self.cognitive.transition("understand","intent and context")
        predicted=self.predictor.predict(message)
        if predicted: self._maybe_preload(predicted)
        system_msg=PERSONAS.get(self.persona,PERSONAS["default"])
        rag_context=''
        if self.rag3:
            try: rag_context=self.rag3.retrieve(message).context
            except Exception as exc: self.logger.warn('rag_retrieval_failed',{'error':str(exc)})
        if rag_context: system_msg += f"\n\nRetrieved context:\n{rag_context}"
        full_history=[{"role":"system","content":system_msg}]+history
        self.cognitive.transition("plan","select execution strategy")
        if task_type=="complex" or self.orchestrator.is_complex(message):
            aion_goal=None
            try:
                aion_goal=self.aion_planner.create_goal(message,priority=0.7,metadata={"session_id":session_id})
                self.aion_planner.plan(aion_goal["id"])
            except Exception:pass
            result=self.orchestrator.run(message,full_history,self.memory)
        else:
            if self.cfg.get("react",{}).get("enabled",False): result=self.react.run(message,history=full_history)
            else: result=self.router.chat(message,history=full_history)
        verification=self.verifier.verify(result)
        try:
            route=self.router.get_stats().get("last_route")
            if self.learned_router and route: self.learned_router.record_performance(route, 0.0, float(verification.get("score",0.0)))
        except Exception: pass
        self.cognitive.transition("verify","response produced")
        if self.memory:
            self.memory.add_message("user",message,session_id=session_id)
            self.memory.add_message("assistant",result,session_id=session_id,embed=True)
        self.cognitive.transition("learn","record interaction")
        try:
            if self.aion3:
                reward=float(verification.get('score',0.0)); self.aion3.record_experience(message,task_type,result,reward,bool(verification.get('verified',False)))
                if 'aion_goal' in locals() and aion_goal:
                    try:self.aion_planner.evaluate(aion_goal["id"],reward)
                    except Exception:pass
        except Exception: pass
        self.cognitive.transition("idle","request complete")
        return result

    def chat_stream(self, message: str, task_type: str="default", session_id: str="default"):
        self.swarm.update_capacity(self.profiler.vram_free_gb)
        self.cognitive.transition("perceive","new user request")
        history=self.memory.get_history(session_id=session_id,limit=self.cfg.get("memory",{}).get("max_history",100)) if self.memory else []
        self.cognitive.transition("understand","intent and context")
        predicted=self.predictor.predict(message)
        if predicted: self._maybe_preload(predicted)
        system_msg=PERSONAS.get(self.persona,PERSONAS["default"])
        rag_context=''
        if self.rag3:
            try: rag_context=self.rag3.retrieve(message).context
            except Exception as exc: self.logger.warn('rag_retrieval_failed',{'error':str(exc)})
        if rag_context: system_msg += f"\n\nRetrieved context:\n{rag_context}"
        full_history=[{"role":"system","content":system_msg}]+history
        self.cognitive.transition("plan","select execution strategy")
        if task_type=="complex" or self.orchestrator.is_complex(message) or self.cfg.get("react",{}).get("enabled",False):
            result=self.chat(message,stream=False,task_type=task_type,session_id=session_id); yield result; return
        chunks=[]
        for chunk in self.router.chat_stream(message,history=full_history):
            text=getattr(chunk,"content","")
            if text: chunks.append(text); yield text
        result="".join(chunks)
        verification=self.verifier.verify(result)
        try:
            route=self.router.get_stats().get("last_route")
            if self.learned_router and route: self.learned_router.record_performance(route, 0.0, float(verification.get("score",0.0)))
        except Exception: pass
        self.cognitive.transition("verify","response produced")
        if self.memory:
            self.memory.add_message("user",message,session_id=session_id)
            self.memory.add_message("assistant",result,session_id=session_id,embed=True)
        self.cognitive.transition("learn","record interaction")
        try:
            if self.aion3:
                reward=float(verification.get('score',0.0)); self.aion3.record_experience(message,task_type,result,reward,bool(verification.get('verified',False)))
                if 'aion_goal' in locals() and aion_goal:
                    try:self.aion_planner.evaluate(aion_goal["id"],reward)
                    except Exception:pass
        except Exception as exc: self.logger.warn("aion_record_experience_failed",{"error":str(exc)})
        self.cognitive.transition("idle","request complete")

    def _maybe_preload(self, model_name: str):
        def _load():
            try: self.swarm.load(model_name,self.cfg.get("native",{})); self.logger.info("predictive_preload",{"model":model_name})
            except Exception as e: self.logger.warn("predictive_preload_failed",{"model":model_name,"error":str(e)})
        if self._preload_thread and self._preload_thread.is_alive(): return
        self._preload_thread=threading.Thread(target=_load,daemon=True); self._preload_thread.start()

    def run_cli(self):
        try:
            from rich.console import Console
            from rich.markdown import Markdown
            console=Console()
        except ImportError:
            console=None; print("rich not installed, using plain output")
        if console: console.print(f"[bold green]JARVIS v{self.version} ready.[/bold green] Type /help for commands.")
        else: print(f"JARVIS v{self.version} ready. Type /help for commands.")
        while True:
            try:
                msg=input("You: ").strip()
                if not msg: continue
                if msg.startswith("/"):
                    if self._handle_command(msg): break
                    continue
                reply=self.chat(msg,stream=False)
                if console: console.print(f"[bold cyan]JARVIS:[/bold cyan] {reply}")
                else: print(f"JARVIS: {reply}")
            except KeyboardInterrupt: break
            except Exception as e:
                if console: console.print(f"[red]Error: {e}[/red]")
                else: print(f"Error: {e}")
        self.shutdown()

    def _handle_command(self, cmd: str) -> bool:
        parts=cmd.split(); verb=parts[0].lower()
        if verb=="/exit": return True
        if verb=="/help":
            print("""Commands:
/models          List discovered models
/load <name>     Load a model
/unload          Unload current model
/swarm <on|off>  Toggle model swarm
/react <on|off>  Toggle ReAct loop
/persona <name>  Switch persona
/session <name>  Switch chat session
/sessions        List sessions
/clear           Clear session memory
/eval            Run evaluation suite
/consolidate     Force memory consolidation
/awareness       Re-index own codebase
/auto <desc>     Auto-generate a tool
/lora            List LoRA adapters
/lora load <n>   Load LoRA adapter
/export <fmt>    Export session (md/json)
/import <path>   Import session
/listen          Enter voice mode
/distributed     Show distributed workers
/resources       Show CPU/RAM/GPU resources
/aion            Show AION cognitive state
/mission <title> Create a persistent mission
/workflow        Show workflow engine status
/discover        Discover local model files
/self-edit <f> <old> <new>  Edit source (dry-run)
/doctor          Run compatibility diagnostics
/bench <task>    Run model benchmark lab
/gpu             Show multi-GPU scheduler state
/rag <query>     Run RAG 3.0 retrieval
/goals           Show AION 3 priorities
/platform        Show cognitive platform status
/certify         Run hardware certification
""")
        elif verb=="/models":
            for m in self.loader.discover():
                fit="✓ fits" if m.estimated_vram_gb<=self.profiler.vram_free_gb else "✗ too large"
                print(f"  {m.name} ({m.param_count}B, {m.quant}, {m.estimated_vram_gb:.1f}GB) {fit}")
        elif verb=="/load" and len(parts)>1:
            try: self.router.set_primary(parts[1]); print(f"Loaded {parts[1]}")
            except Exception as e: print(f"Load failed: {e}")
        elif verb=="/unload": self.router.unload_primary(); print("Unloaded.")
        elif verb=="/swarm":
            on=len(parts)>1 and parts[1]=="on"; self.cfg["model_swarm"]={"enabled":on}; print(f"Swarm {'enabled' if on else 'disabled'}.")
        elif verb=="/react":
            on=len(parts)>1 and parts[1]=="on"; self.cfg.setdefault("react",{})["enabled"]=on; print(f"ReAct {'enabled' if on else 'disabled'}.")
        elif verb=="/persona" and len(parts)>1:
            self.persona=parts[1] if parts[1] in PERSONAS else "default"; print(f"Persona: {self.persona}")
        elif verb=="/session" and len(parts)>1:
            self.current_session=parts[1]; self.memory.get_history(self.current_session,limit=1) if self.memory else None; print(f"Session: {self.current_session}")
        elif verb=="/sessions": print(f"Sessions: {self.memory.list_sessions() if self.memory else ['default']}")
        elif verb=="/clear":
            if self.memory: self.memory.clear_session(self.current_session)
            print("Session cleared.")
        elif verb=="/eval":
            try:
                from tests.eval_runner import run_evaluation
                print(run_evaluation(self))
            except Exception as e: print(f"Eval error: {e}")
        elif verb=="/consolidate":
            if self.consolidator:
                try: self.consolidator.run(); print("Consolidation complete.")
                except Exception as e: print(f"Consolidation error: {e}")
            else: print("Consolidator not available.")
        elif verb=="/awareness":
            if self.self_aware:
                try: self.self_aware.scan(); print("Self-awareness scan complete.")
                except Exception as e: print(f"Awareness error: {e}")
            else: print("Self-awareness not available.")
        elif verb=="/auto" and len(parts)>1:
            try: result=self.auto_programmer.generate_tool(" ".join(parts[1:])); print(result)
            except Exception as e: print(f"Auto-programmer error: {e}")
        elif verb=="/lora" and len(parts)>2 and parts[1]=="load":
            try: self.lora.load_adapter(parts[2]); print(f"Loaded LoRA: {parts[2]}")
            except Exception as e: print(f"LoRA load error: {e}")
        elif verb=="/lora":
            try: adapters=self.lora.list_adapters(); print(adapters)
            except Exception as e: print(f"LoRA error: {e}")
        elif verb=="/export" and len(parts)>1:
            if self.memory:
                try:
                    from memory.export_import import Exporter
                    print(Exporter(self.memory,self.cfg.get("security",{}).get("workspace_root","data/workspace")).export_session(getattr(self,"current_session","default"),parts[1]))
                except Exception as e:print(f"Export error: {e}")
            else: print("Memory not available.")
        elif verb=="/import" and len(parts)>1:
            if self.memory:
                try:
                    from memory.export_import import Importer
                    print(Importer(self.memory,self.cfg.get("security",{}).get("workspace_root","data/workspace")).import_file(parts[1]))
                except Exception as e: print(f"Import error: {e}")
            else: print("Memory not available.")
        elif verb=="/listen":
            if self.voice_loop: print("Voice mode started."); self.voice_loop.start()
            else: print("Voice loop not available.")
        elif verb=="/distributed":
            if self.distributed: print(self.distributed.get_cluster_stats())
            else: print("Distributed backend not enabled.")
        elif verb=="/resources":
            snap=self.resources.snapshot(); print(json.dumps(snap,indent=2,default=str))
        elif verb=="/aion":
            if self.aion3: print(self.aion3.get_stats())
            else: print("AION not available.")
        elif verb=="/mission" and len(parts)>1:
            try: m=self.missions.create(" ".join(parts[1:])); print(f"Mission created: {m.mission_id}")
            except Exception as e: print(f"Mission error: {e}")
        elif verb=="/workflow":
            print(self.workflows.get_stats() if hasattr(self.workflows,'get_stats') else "Workflow engine active.")
        elif verb=="/discover":
            models=self.model_discovery.scan(); print(f"Discovered {len(models)} models")
            for m in models: print(f"  {m.name}")
        elif verb=="/self-edit" and len(parts)>=4:
            try: result=self.self_edit_guard.propose(parts[1],parts[2],parts[3]); print(result)
            except Exception as e: print(f"Self-edit error: {e}")
        elif verb=="/doctor":
            d=Doctor(); d.run_all(); print(json.dumps(d.get_report(),indent=2))
        elif verb=="/bench" and len(parts)>1:
            if self.benchmark_lab:
                try: print(self.benchmark_lab.run_suite(parts[1],router=self.router))
                except Exception as e: print(f"Benchmark error: {e}")
            else: print("Benchmark lab not available.")
        elif verb=="/gpu":
            print(self.multi_gpu.get_stats() if hasattr(self.multi_gpu,'get_stats') else "GPU runtime active.")
        elif verb=="/rag" and len(parts)>1:
            if self.rag3:
                try: result=self.rag3.retrieve(" ".join(parts[1:])); print(result)
                except Exception as e: print(f"RAG error: {e}")
            else: print("RAG engine not available.")
        elif verb=="/goals":
            if self.aion3:
                goal=self.aion3.suggest_goal(); print(goal or "No goals suggested.")
            else: print("AION planner not available.")
        elif verb=="/platform":
            print(self.cognitive.reflect() if hasattr(self.cognitive,'reflect') else "Cognitive platform active.")
        elif verb=="/certify":
            print(self.hardware_cert.get_report())
        return False

    def shutdown(self):
        self._shutdown=True
        self.logger.info("jarvis_shutdown",{"version":self.version})
        self.router.unload_all()
        self.swarm.shutdown()
        self.multi_gpu.shutdown()
        if self.distributed: self.distributed.shutdown()
        if self.event_bus: self.event_bus.shutdown()
        for t in self._threads:
            if hasattr(t,'stop'):
                try:t.stop()
                except Exception:pass
        for obj in (getattr(self,"watchdog",None),getattr(self,"aion_bridge",None),getattr(self,"voice_loop",None),getattr(self,"distributed",None),getattr(self,"orchestrator",None),getattr(self,"workflows",None),getattr(self,"memory",None)):
            if obj and hasattr(obj,"shutdown"):
                try:obj.shutdown()
                except Exception:pass
            elif obj and hasattr(obj,"close"):
                try:obj.close()
                except Exception:pass

    def get_stats(self) -> dict:
        return {"version":self.version,"persona":self.persona,"models_loaded":len(self.swarm.loaded),
                "memory_sessions":len(self.memory.list_sessions()) if self.memory else 0,
                "import_errors":len(_IMPORT_ERRORS)}

def main():
    parser=argparse.ArgumentParser(description="JARVIS v12.1.2")
    parser.add_argument("--config",help="Path to config.json")
    parser.add_argument("--api",action="store_true",help="Start API server")
    parser.add_argument("--gui",action="store_true",help="Start GUI")
    parser.add_argument("--doctor",action="store_true",help="Run diagnostics and exit")
    args=parser.parse_args()
    if args.doctor:
        d=Doctor(); d.run_all(); print(json.dumps(d.get_report(),indent=2)); return
    cfg=load_config(args.config)
    core=JARVISCore(cfg)
    if args.api:
        try:
            import uvicorn
            from api.server import configure_core
            configure_core(core)
            api_cfg=cfg.get("api",{})
            host=str(api_cfg.get("host","127.0.0.1"))
            port=int(api_cfg.get("port",8000))
            if host not in {"127.0.0.1","localhost","::1"} and not os.environ.get("JARVIS_API_TOKEN"):
                raise RuntimeError("JARVIS_API_TOKEN (>=32 chars) is required for non-loopback API binding")
            uvicorn.run(fastapi_app,host=host,port=port,log_level="info")
        except ImportError: print("uvicorn not installed. Run: pip install uvicorn")
    elif args.gui:
        try:
            from gui.flet_app import FletApp
            FletApp(core).run()
        except Exception as e: print(f"GUI error: {e}")
    else: core.run_cli()

if __name__=="__main__": main()
