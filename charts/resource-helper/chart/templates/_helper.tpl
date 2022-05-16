{{/*
Will return the Values.nameOverride or the Release.Name
*/}}
{{- define "helper.name" -}}
{{- default .Release.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
Will return the project name
*/}}
{{- define "helper.project.name" -}}
{{- printf "%s-%s" (include "helper.name" . ) .Values.project.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Will return the resourceQuota name
*/}}
{{- define "helper.resourceQuota.name" -}}
{{- printf "%s-%s" (include "helper.name" .context ) .name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Will return the networkPolicy name
*/}}
{{- define "helper.networkPolicy.name" -}}
{{- printf "%s-%s" (include "helper.name" . ) .Values.networkPolicy.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "helper.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "helper.labels" -}}
helm.sh/chart: {{ include "helper.chart" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: {{ .Release.Name }}
{{- with .Values.global.additionalLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}
