import streamlit as st
import time
from examples import EXAMPLES

st.set_page_config(page_title="Architecture Pipeline", layout="wide")

st.title("Architecture Pipeline — AI-Powered Technical Spec Generator")
st.caption("Powered by a multi-agent CrewAI system with 4 specialized AI agents")

# ── Section 1: Input ──────────────────────────────────────────

if "requirement_text" not in st.session_state:
    st.session_state.requirement_text = ""

cols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    if cols[i].button(ex["label"], use_container_width=True):
        st.session_state.requirement_text = ex["requirement"]

requirement = st.text_area(
    "Business Requirement",
    value=st.session_state.requirement_text,
    height=200,
    placeholder="Enter a high-level business requirement...",
)

if st.button("Analyze & Generate", type="primary", disabled=not requirement.strip()):
    start = time.time()

    from crew import run_crew, AGENT_STEPS

    progress_bar = st.progress(0, text="Initializing CrewAI pipeline...")
    status_area = st.container()

    # Create placeholders for each agent step
    placeholders = []
    with status_area:
        for i, step in enumerate(AGENT_STEPS):
            placeholders.append(st.empty())
            if i == 0:
                placeholders[i].info(f"🔄 **Agent {i+1}/4 — {step['label']}**: {step['description']}")
            else:
                placeholders[i].markdown(f"⏳ **Agent {i+1}/4 — {step['label']}**: Waiting...")

    completed_count = [0]

    def on_task_complete(idx, step, output):
        completed_count[0] += 1
        # Mark current task as done
        placeholders[idx].success(f"✅ **Agent {idx+1}/4 — {step['label']}**: Complete")
        # Mark next task as running
        next_idx = idx + 1
        if next_idx < len(AGENT_STEPS):
            next_step = AGENT_STEPS[next_idx]
            placeholders[next_idx].info(
                f"🔄 **Agent {next_idx+1}/4 — {next_step['label']}**: {next_step['description']}"
            )
        # Update progress bar
        progress_bar.progress(
            completed_count[0] / len(AGENT_STEPS),
            text=f"Completed {completed_count[0]}/{len(AGENT_STEPS)} agents..."
        )

    result = run_crew(requirement.strip(), on_task_complete=on_task_complete)

    elapsed = time.time() - start

    if result.get("error"):
        progress_bar.progress(1.0, text="Pipeline failed.")
        # Mark remaining agents as failed
        for i, step in enumerate(AGENT_STEPS):
            if result.get(step["key"]) is None:
                placeholders[i].error(f"❌ **Agent {i+1}/4 — {step['label']}**: Failed")
        st.error(f"Agent pipeline failed: {result['error']}. Please try again.")
    else:
        progress_bar.progress(1.0, text=f"Pipeline complete in {elapsed:.1f}s!")
        st.success(f"Completed in {elapsed:.1f}s")

        # ── Section 2: Planner Output ─────────────────────────────
        analysis = result["analysis"]
        if analysis:
            with st.expander("Requirement Analysis", expanded=True):
                st.subheader(analysis.project_name)
                st.write(analysis.summary)

                if analysis.assumptions:
                    st.info("**Assumptions:** " + " • ".join(analysis.assumptions))

                st.markdown("#### Modules")
                module_data = [
                    {
                        "Module": m.name,
                        "Responsibility": m.responsibility,
                        "Dependencies": ", ".join(m.depends_on) if m.depends_on else "None",
                    }
                    for m in analysis.modules
                ]
                st.table(module_data)

                st.markdown("#### Entities")
                for e in analysis.entities:
                    st.markdown(f"**{e.name}** — {e.description}")
                    if e.relationships:
                        st.markdown(
                            "  " + ", ".join(e.relationships)
                        )

                st.markdown("#### Suggested Tech Stack")
                ts = analysis.suggested_tech_stack
                st.markdown(
                    f"**Backend:** {ts.backend} | **Database:** {ts.database} | **Auth:** {ts.auth}"
                )
        else:
            st.warning("Requirement analysis generation failed.")

        # ── Section 3: Technical Specification ────────────────────
        tab_db, tab_api, tab_code = st.tabs(
            ["Database Schemas", "API Specification", "Pseudocode"]
        )

        # Tab 1: Database Schemas
        with tab_db:
            schemas = result["schemas"]
            if schemas:
                for schema in schemas.schemas:
                    st.subheader(schema.entity)

                    st.markdown("**Properties**")
                    prop_data = []
                    for name, prop in schema.properties.items():
                        prop_data.append(
                            {
                                "Field": name,
                                "Type": prop.type,
                                "Format": prop.format or "—",
                                "Description": prop.description,
                                "Required": "Yes"
                                if name in schema.required_fields
                                else "",
                            }
                        )
                    st.table(prop_data)

                    if schema.relationships:
                        st.markdown("**Relationships**")
                        for rel_name, rel in schema.relationships.items():
                            st.markdown(
                                f"- **{rel_name}**: {rel.type} → `{rel.target}` (FK: `{rel.foreign_key}`)"
                            )
                    st.divider()
            else:
                st.warning("Database schema generation failed.")

        # Tab 2: API Specification
        with tab_api:
            api = result["api"]
            if api:
                st.markdown(f"**Base URL:** `{api.base_url}`")

                # Group endpoints by module
                modules = {}
                for ep in api.endpoints:
                    modules.setdefault(ep.module, []).append(ep)

                for module_name, endpoints in modules.items():
                    st.subheader(module_name)
                    for ep in endpoints:
                        method_colors = {
                            "GET": "green",
                            "POST": "blue",
                            "PUT": "orange",
                            "PATCH": "orange",
                            "DELETE": "red",
                        }
                        color = method_colors.get(ep.method.upper(), "gray")
                        auth_badge = " :lock:" if ep.auth_required else ""

                        st.markdown(
                            f":{color}[**{ep.method.upper()}**] `{ep.path}` — {ep.description}{auth_badge}"
                        )

                        with st.expander(f"Details: {ep.method.upper()} {ep.path}"):
                            if ep.request_body:
                                st.markdown("**Request Body**")
                                st.json(ep.request_body)
                            if ep.query_params:
                                st.markdown("**Query Parameters**")
                                st.json(ep.query_params)
                            st.markdown("**Success Response**")
                            st.json(ep.response_success)
                            st.markdown("**Error Response**")
                            st.json(ep.response_error)
            else:
                st.warning("API specification generation failed.")

        # Tab 3: Pseudocode
        with tab_code:
            pseudocode = result["pseudocode"]
            if pseudocode:
                for mod in pseudocode.modules:
                    st.subheader(mod.module_name)
                    for fn in mod.functions:
                        st.markdown(f"**{fn.name}** — {fn.description}")
                        st.code(fn.pseudocode, language="python")
            else:
                st.warning("Pseudocode generation failed.")
