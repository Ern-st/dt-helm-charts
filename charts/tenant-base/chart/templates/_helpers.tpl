{{/*
Common labels
Takes a dictionary contaning containing:
 - 'name'=<The name to use in the labels>,
 - 'values'=<The map of the relative values from a loop>,
 - 'root'=<The root values - used to access ".Release.Name"> - optional - if not present the value will be retrived from .values
*/}}
{{- define "chart.labels" -}}
{{ include "chart.selectorLabels" (dict "name" .name)}}
{{- if .values }}
app.kubernetes.io/version: {{ .values.image.tag }}
{{- end }}
app.kubernetes.io/part-of: {{ .root.Release.Name }}
{{- end }}

{{/*
SelectorLabels
Takes a dictionary contaning containing: 'name'=string
*/}}
{{- define "chart.selectorLabels" -}}
app.kubernetes.io/name: {{ .name }}
app.kubernetes.io/instance: {{ .name }}
{{- end }}

{{/*
template for topologySpredConstrains
*/}}
{{- define "chart.topologySpreadConstrains" -}}
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        {{- include "chart.selectorLabels" (dict "name" .name) | nindent 8 }}
{{- end }}
