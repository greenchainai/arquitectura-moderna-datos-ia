SELECT
    ra.recommendation_type,
    fe.outcome,
    COUNT(*) AS total_events
FROM decisioning.recommended_action ra
JOIN decisioning.decision_log dl ON ra.recommendation_id = dl.recommendation_id
JOIN decisioning.feedback_event fe ON dl.decision_id = fe.decision_id
GROUP BY ra.recommendation_type, fe.outcome
ORDER BY ra.recommendation_type, fe.outcome;

SELECT *
FROM decisioning.decision_log
WHERE decision_status = 'PENDING_APPROVAL';
